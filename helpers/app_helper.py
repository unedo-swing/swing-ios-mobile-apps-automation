from pathlib import Path

from config.settings import settings
from helpers.logger import get_logger

log = get_logger("app")

RESET_STRATEGIES = ("force_close", "clear", "reinstall", "none")

_STRATEGY_ALIASES = {
    "force_close": "force_close",
    "forceclose": "force_close",
    "restart": "force_close",
    "terminate": "force_close",
    "clear": "clear",
    "clear_data": "clear",
    "wipe": "clear",
    "reinstall": "reinstall",
    "install": "reinstall",
    "full_reset": "reinstall",
    "none": "none",
    "off": "none",
    "skip": "none",
}


def _session_cap(driver, name):
    caps = getattr(driver, "capabilities", None) or {}
    return caps.get(name) or caps.get(f"appium:{name}")


def bundle_of(driver=None, bundle_id=None):
    target = bundle_id or _session_cap(driver, "bundleId") or settings.BUNDLE_ID
    if not target:
        raise ValueError("bundle id is not configured")
    return target


def app_path_of(driver=None, app_path=None):
    return app_path or _session_cap(driver, "app") or settings.APP_PATH


def _bundle(bundle_id=None, driver=None):
    return bundle_of(driver, bundle_id)


def install(driver, app_path):
    driver.install_app(app_path)
    log.info(f"installed {app_path}")


def uninstall(driver, bundle_id=None):
    driver.remove_app(_bundle(bundle_id, driver))


def is_installed(driver, bundle_id=None):
    return driver.is_app_installed(_bundle(bundle_id, driver))


def activate(driver, bundle_id=None):
    driver.activate_app(_bundle(bundle_id, driver))


def terminate(driver, bundle_id=None):
    return driver.terminate_app(_bundle(bundle_id, driver))


def force_close(driver, bundle_id=None):
    target = _bundle(bundle_id, driver)
    driver.terminate_app(target)
    driver.activate_app(target)
    log.info(f"force-closed {target}")
    return target


def _blocked_on_real_device(action):
    if settings.is_real_device() and not settings.REAL_DEVICE_ALLOW_CLEAR:
        log.warning(f"{action} is disabled on a real device, falling back to force-close")
        return True
    return False


def clear_data(driver, bundle_id=None):
    target = _bundle(bundle_id, driver)
    driver.terminate_app(target)
    driver.execute_script("mobile: clearApp", {"bundleId": target})
    driver.activate_app(target)
    log.info(f"cleared data of {target}")
    return target


def clear(driver, bundle_id=None, app_path=None):
    target = _bundle(bundle_id, driver)
    if not settings.is_real_device():
        return clear_data(driver, target)
    if _blocked_on_real_device("clear"):
        return force_close(driver, target)
    path = app_path_of(driver, app_path)
    if not path:
        log.warning(f"APP_PATH not set, clear falls back to force-close for {target}")
        return force_close(driver, target)
    if not Path(path).exists():
        log.warning(f"APP_PATH {path} does not exist, clear falls back to force-close for {target}")
        return force_close(driver, target)
    driver.terminate_app(target)
    driver.remove_app(target)
    try:
        driver.install_app(path)
    except Exception as exc:
        raise RuntimeError(
            f"{target} was removed from the device and could not be reinstalled from {path}: {exc}"
        ) from exc
    driver.activate_app(target)
    log.info(f"cleared {target} by reinstalling (real devices have no clear-data api)")
    return target


def reinstall(driver, bundle_id=None, app_path=None):
    target = _bundle(bundle_id, driver)
    if _blocked_on_real_device("reinstall"):
        return force_close(driver, target)
    path = app_path_of(driver, app_path)
    if not path:
        raise ValueError("APP_PATH is required for the reinstall strategy")
    try:
        driver.terminate_app(target)
    except Exception as exc:
        log.warning(f"terminate before reinstall failed: {exc}")
    if driver.is_app_installed(target):
        driver.remove_app(target)
    driver.install_app(path)
    driver.activate_app(target)
    log.info(f"reinstalled {target}")
    return target


def normalize_strategy(name=None):
    raw = name if name else settings.app_reset_strategy()
    key = str(raw).strip().lower().replace("-", "_")
    if key not in _STRATEGY_ALIASES:
        raise ValueError(
            f"unknown app reset strategy: {raw} (use {', '.join(RESET_STRATEGIES)})"
        )
    return _STRATEGY_ALIASES[key]


def reset(driver, strategy=None, bundle_id=None, app_path=None):
    name = normalize_strategy(strategy)
    if name == "none":
        log.info("app reset skipped")
        return None
    if name == "clear":
        return clear(driver, bundle_id, app_path)
    if name == "reinstall":
        return reinstall(driver, bundle_id, app_path)
    return force_close(driver, bundle_id)


def restart(driver, bundle_id=None):
    return force_close(driver, bundle_id)


def app_state(driver, bundle_id=None):
    return driver.query_app_state(_bundle(bundle_id, driver))


def is_running_foreground(driver, bundle_id=None):
    return app_state(driver, bundle_id) == 4


def clear_and_relaunch(driver, bundle_id=None, app_path=None):
    return clear(driver, bundle_id, app_path)


def launch_settings(driver):
    driver.activate_app("com.apple.Preferences")


def launch_safari(driver):
    driver.activate_app("com.apple.mobilesafari")


def install_certificate(driver, content, name="cert"):
    driver.execute_script(
        "mobile: installCertificate", {"content": content, "commonName": name}
    )


def list_apps(driver):
    return driver.execute_script("mobile: listApps")
