import json

from config.settings import settings


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

    if settings.EXTRA_CAPS:
        caps.update(json.loads(settings.EXTRA_CAPS))
    if overrides:
        caps.update(overrides)
    return caps
