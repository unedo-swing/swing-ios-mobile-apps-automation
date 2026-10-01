import pytest

from config.settings import settings
from helpers import app_helper
from helpers.logger import get_logger

log = get_logger("fixture")


def _marker(request):
    return request.node.get_closest_marker("app_reset")


def _recover(driver, target, error):
    if app_helper.is_installed(driver, target):
        log.warning(f"falling back to force-close for {target}")
        return app_helper.force_close(driver, target)
    path = app_helper.app_path_of(driver)
    log.warning(f"{target} is not installed any more, reinstalling from {path}")
    app_helper.install(driver, path)
    app_helper.activate(driver, target)
    return target


def apply_reset(request, driver):
    if getattr(request.node, "app_reset_done", False):
        return None
    marker = _marker(request)
    raw = None
    bundle_id = None
    if marker:
        raw = marker.args[0] if marker.args else marker.kwargs.get("strategy")
        bundle_id = marker.kwargs.get("bundle_id")
    target = app_helper.bundle_of(driver, bundle_id)
    log.info(f"app reset {app_helper.normalize_strategy(raw)} for {target}")
    try:
        result = app_helper.reset(driver, raw, target)
    except Exception as exc:
        log.warning(f"app reset failed ({type(exc).__name__}: {exc})")
        result = _recover(driver, target, exc)
    request.node.app_reset_done = True
    return result


@pytest.fixture
def app_reset_strategy(request):
    marker = _marker(request)
    raw = None
    if marker:
        raw = marker.args[0] if marker.args else marker.kwargs.get("strategy")
    if raw is None:
        raw = getattr(request, "param", None)
    return app_helper.normalize_strategy(raw)


@pytest.fixture
def app_bundle_id(request):
    marker = _marker(request)
    if marker and marker.kwargs.get("bundle_id"):
        return marker.kwargs["bundle_id"]
    return settings.BUNDLE_ID


@pytest.fixture
def app(request, driver):
    apply_reset(request, driver)
    return driver


@pytest.fixture
def force_close_app(driver):
    def run(bundle_id=None):
        return app_helper.force_close(driver, bundle_id)

    return run


@pytest.fixture
def clear_app(driver):
    def run(bundle_id=None, app_path=None):
        return app_helper.clear(driver, bundle_id, app_path)

    return run


@pytest.fixture
def reinstall_app(driver):
    def run(bundle_id=None, app_path=None):
        return app_helper.reinstall(driver, bundle_id, app_path)

    return run


@pytest.fixture
def reset_app(driver):
    def run(strategy=None, bundle_id=None, app_path=None):
        return app_helper.reset(driver, strategy, bundle_id, app_path)

    return run
