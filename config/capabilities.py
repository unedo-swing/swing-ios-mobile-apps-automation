import json
import os
from pathlib import Path

from config.settings import ROOT_DIR, settings


def build_capabilities(overrides=None):
    if settings.is_real_device() and not settings.UDID:
        raise ValueError("UDID is required when TARGET=real_device")
    if not settings.BUNDLE_ID:
        raise ValueError("BUNDLE_ID is required")

    caps = {
        "platformName": settings.PLATFORM_NAME,
        "appium:automationName": settings.AUTOMATION_NAME,
        "appium:deviceName": settings.DEVICE_NAME,
        "appium:platformVersion": settings.PLATFORM_VERSION,
        "appium:udid": settings.UDID,
        "appium:deviceId": settings.UDID,
        "appium:bundleId": settings.BUNDLE_ID,
        "appium:noReset": settings.NO_RESET,
        "appium:isHeadless": True
    }
    caps = {key: value for key, value in caps.items() if value not in (None, "")}
    if settings.WDA_LOCAL_PORT:
        caps["appium:wdaLocalPort"] = settings.WDA_LOCAL_PORT
    if settings.MJPEG_PORT:
        caps["appium:mjpegServerPort"] = settings.MJPEG_PORT
    if settings.APP_MODE == "app_path" and settings.APP_PATH:
        caps["appium:app"] = settings.APP_PATH

    if settings.EXTRA_CAPS:
        caps.update(json.loads(settings.EXTRA_CAPS))
    if overrides:
        caps.update(overrides)
    return caps


def resolve_app_path(value):
    if not value:
        return None
    path = Path(value).expanduser()
    return str(path if path.is_absolute() else ROOT_DIR / path)


def device_overrides(device):
    prefix = f"DEVICE_{device}_"
    udid = os.getenv(f"{prefix}UDID")
    if not udid:
        raise ValueError(f"@pytest.mark.device({device}) needs {prefix}UDID in the env file")
    caps = {
        "appium:udid": udid,
        "appium:deviceId": udid,
        "appium:deviceName": os.getenv(f"{prefix}DEVICE_NAME"),
        "appium:platformVersion": os.getenv(f"{prefix}PLATFORM_VERSION"),
        "appium:wdaLocalPort": int(os.getenv(f"{prefix}WDA_LOCAL_PORT") or 0),
        "appium:mjpegServerPort": int(os.getenv(f"{prefix}MJPEG_PORT") or 0),
        "appium:bundleId": os.getenv(f"{prefix}BUNDLE_ID"),
        "appium:app": resolve_app_path(os.getenv(f"{prefix}APP_PATH")),
    }
    caps = {key: value for key, value in caps.items() if value not in (None, "", 0)}
    if os.getenv(f"{prefix}EXTRA_CAPS"):
        caps.update(json.loads(os.environ[f"{prefix}EXTRA_CAPS"]))
    return caps


def marker_device(markers):
    return next((mark.args[0] for mark in markers if mark.args), None)


def marker_app(markers):
    return next((mark.kwargs["app"] for mark in markers if mark.kwargs.get("app")), None)
