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


@pytest.fixture(scope="function")
def driver(request):
    overrides = getattr(request, "param", None)
    instance = create_driver(overrides)
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


def player_capabilities():
    if not (settings.PLAYER_UDID or settings.PLAYER_DEVICE_NAME):
        raise ValueError("PLAYER_UDID or PLAYER_DEVICE_NAME is required for the player device")
    caps = {
        "appium:udid": settings.PLAYER_UDID,
        "appium:deviceId": settings.PLAYER_UDID,
        "appium:deviceName": settings.PLAYER_DEVICE_NAME,
        "appium:platformVersion": settings.PLAYER_PLATFORM_VERSION,
        "appium:wdaLocalPort": settings.PLAYER_WDA_LOCAL_PORT,
        "appium:mjpegServerPort": settings.PLAYER_MJPEG_PORT,
    }
    return {key: value for key, value in caps.items() if value not in (None, "")}


@pytest.fixture(scope="function")
def player_driver(request):
    from helpers import app_helper

    instance = create_driver(player_capabilities())
    marker = request.node.get_closest_marker("app_reset")
    if marker:
        strategy = marker.args[0] if marker.args else marker.kwargs.get("strategy")
        try:
            bundle_id = marker.kwargs.get("bundle_id")
            if settings.PLAYER_TARGET == "simulator" and app_helper.normalize_strategy(strategy) == "clear":
                app_helper.clear_data(instance, bundle_id)
            else:
                app_helper.reset(instance, strategy, bundle_id)
        except Exception as exc:
            log.warning(f"player app reset failed ({type(exc).__name__}: {exc})")
            app_helper.activate(instance)
    request.node.player_driver = instance
    yield instance
    if getattr(request.node, "test_failed", False) and settings.SCREENSHOT_ON_FAILURE:
        try:
            media.screenshot(instance, f"{request.node.name}_player")
        except Exception as exc:
            log.warning(f"player screenshot failed: {exc}")
    quit_driver(instance)
