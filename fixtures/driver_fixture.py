import pytest

from config.settings import settings
from helpers import media
from helpers.driver_factory import create_driver, quit_driver
from helpers.logger import get_logger
from helpers.reporter import reporter

log = get_logger("fixture")


@pytest.fixture(scope="session")
def app_settings():
    return settings


@pytest.fixture(scope="session")
def session_driver():
    driver = create_driver()
    yield driver
    quit_driver(driver)


def driver_overrides(request):
    import os

    from config.capabilities import device_overrides, marker_app, marker_device, resolve_app_path
    from config.settings import worker_index

    markers = list(request.node.iter_markers("device"))
    device = marker_device(markers)
    app = marker_app(markers)
    index = worker_index()
    if device is None and index is not None and not os.getenv(f"WORKER_{index}_UDID"):
        pytest.fail(f"{request.node.name} has no @pytest.mark.device(<n>) and worker gw{index} "
                    f"has no WORKER_{index}_UDID, so it would share a simulator with another worker")
    overrides = device_overrides(device) if device is not None else {}
    if app:
        path = resolve_app_path(app)
        if not os.path.exists(path):
            pytest.fail(f"@pytest.mark.device app not found: {path}")
        overrides.update({"appium:app": path, "appium:enforceAppInstall": True})
    overrides.update(getattr(request, "param", None) or {})
    return overrides or None


@pytest.fixture(scope="function")
def driver(request):
    instance = create_driver(driver_overrides(request))
    if settings.VIDEO_ON_FAILURE:
        try:
            media.start_recording(instance)
        except Exception as exc:
            log.warning(f"recording not started: {exc}")
    request.node.driver = instance
    reporter.bind(instance)
    if request.node.get_closest_marker("app_reset"):
        from fixtures.app_fixtures import apply_reset

        apply_reset(request, instance)
    yield instance
    failed = getattr(request.node, "test_failed", False)
    captured = getattr(request.node, "failure_screenshot", None)
    if failed and settings.SCREENSHOT_ON_FAILURE and not captured:
        try:
            media.screenshot(instance, request.node.name)
        except Exception as exc:
            log.warning(f"screenshot failed: {exc}")
    if settings.VIDEO_ON_FAILURE:
        try:
            if failed:
                media.stop_recording(instance, request.node.name)
            else:
                instance.stop_recording_screen()
        except Exception:
            pass
    reporter.unbind()
    quit_driver(instance)


@pytest.fixture(scope="function")
def fresh_app(driver):
    from helpers import app_helper

    app_helper.reset(driver)
    return driver
