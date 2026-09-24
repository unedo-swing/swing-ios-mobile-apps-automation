import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent


def _load_env():
    explicit = os.getenv("ENV_FILE")
    if explicit:
        load_dotenv(ROOT_DIR / explicit, override=False)
        return
    target = os.getenv("TARGET", "").strip().lower()
    candidates = []
    if target == "real_device":
        candidates = [".env.real_device", ".env"]
    elif target == "simulator":
        candidates = [".env.simulator", ".env"]
    else:
        candidates = [".env"]
    for name in candidates:
        path = ROOT_DIR / name
        if path.exists():
            load_dotenv(path, override=False)
            return


_load_env()


def get(key, default=None):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value


def get_bool(key, default=False):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value.strip().lower() in ("1", "true", "yes", "y", "on")


def get_int(key, default=0):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return int(value)


def get_float(key, default=0.0):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return float(value)


class Settings:
    TARGET = get("TARGET", "simulator").lower()
    PLATFORM_NAME = get("PLATFORM_NAME", "iOS")
    AUTOMATION_NAME = get("AUTOMATION_NAME", "XCUITest")

    APPIUM_HOST = get("APPIUM_HOST", "127.0.0.1")
    APPIUM_PORT = get_int("APPIUM_PORT", 4723)
    APPIUM_PATH = get("APPIUM_PATH", "")

    DEVICE_NAME = get("DEVICE_NAME", "iPhone 15 Pro")
    PLATFORM_VERSION = get("PLATFORM_VERSION")
    UDID = get("UDID")
    XCODE_ORG_ID = get("XCODE_ORG_ID")
    XCODE_SIGNING_ID = get("XCODE_SIGNING_ID", "iPhone Developer")
    UPDATED_WDA_BUNDLE_ID = get("UPDATED_WDA_BUNDLE_ID")

    PLAYER_TARGET = get("PLAYER_TARGET", "simulator").lower()
    PLAYER_UDID = get("PLAYER_UDID")
    PLAYER_DEVICE_NAME = get("PLAYER_DEVICE_NAME")
    PLAYER_PLATFORM_VERSION = get("PLAYER_PLATFORM_VERSION")
    PLAYER_WDA_LOCAL_PORT = get_int("PLAYER_WDA_LOCAL_PORT", 8101)
    PLAYER_MJPEG_PORT = get_int("PLAYER_MJPEG_PORT", 9101)

    APP_MODE = get("APP_MODE", "bundle_id").lower()
    BUNDLE_ID = get("BUNDLE_ID")
    APP_PATH = get("APP_PATH")

    APP_RESET_STRATEGY = get("APP_RESET_STRATEGY", "force_close").lower()
    REAL_DEVICE_ALLOW_CLEAR = get_bool("REAL_DEVICE_ALLOW_CLEAR", False)

    NO_RESET = get_bool("NO_RESET", True)
    FULL_RESET = get_bool("FULL_RESET", False)
    AUTO_ACCEPT_ALERTS = get_bool("AUTO_ACCEPT_ALERTS", False)
    AUTO_DISMISS_ALERTS = get_bool("AUTO_DISMISS_ALERTS", False)
    CONNECT_HARDWARE_KEYBOARD = get_bool("CONNECT_HARDWARE_KEYBOARD", False)
    SHOW_XCODE_LOG = get_bool("SHOW_XCODE_LOG", False)
    USE_NEW_WDA = get_bool("USE_NEW_WDA", False)
    USE_PREBUILT_WDA = get_bool("USE_PREBUILT_WDA", False)
    EXTRA_CAPS = get("EXTRA_CAPS")
    USE_PREINSTALLED_WDA = get_bool("USE_PREINSTALLED_WDA", False)
    PREBUILT_WDA_PATH = get("PREBUILT_WDA_PATH")
    WEBDRIVERAGENT_URL = get("WEBDRIVERAGENT_URL")
    WDA_LOCAL_PORT = get_int("WDA_LOCAL_PORT", 8100)
    WDA_LAUNCH_TIMEOUT = get_int("WDA_LAUNCH_TIMEOUT", 120000)
    WDA_CONNECTION_TIMEOUT = get_int("WDA_CONNECTION_TIMEOUT", 120000)
    WDA_STARTUP_RETRIES = get_int("WDA_STARTUP_RETRIES", 2)
    WDA_STARTUP_RETRY_INTERVAL = get_int("WDA_STARTUP_RETRY_INTERVAL", 20000)
    SWIPE_VELOCITY = get_int("SWIPE_VELOCITY", 400)
    SLOW_SCROLL = get_bool("SLOW_SCROLL", True)
    SWIPE_START_PERCENT = get_int("SWIPE_START_PERCENT", 60)
    SWIPE_END_PERCENT = get_int("SWIPE_END_PERCENT", 40)
    SWIPE_DURATION_MS = get_int("SWIPE_DURATION_MS", 1200)
    MAX_SCROLLS = get_int("MAX_SCROLLS", 8)
    SCROLL_CHECK_TIMEOUT = get_int("SCROLL_CHECK_TIMEOUT", 3)
    SCROLL_DURATION = get_float("SCROLL_DURATION", 1.2)
    SWIPE_PERCENT = get_float("SWIPE_PERCENT", 0.5)
    SCROLL_SETTLE = get_float("SCROLL_SETTLE", 1.0)
    SIMPLE_IS_VISIBLE_CHECK = get_bool("SIMPLE_IS_VISIBLE_CHECK", True)
    SNAPSHOT_MAX_DEPTH = get_int("SNAPSHOT_MAX_DEPTH", 62)
    CUSTOM_SNAPSHOT_TIMEOUT = get_int("CUSTOM_SNAPSHOT_TIMEOUT", 15)
    NEW_COMMAND_TIMEOUT = get_int("NEW_COMMAND_TIMEOUT", 300)
    SETTINGS_LANGUAGE = get("SETTINGS_LANGUAGE")
    SETTINGS_LOCALE = get("SETTINGS_LOCALE")

    IMPLICIT_WAIT = get_float("IMPLICIT_WAIT", 0)
    EXPLICIT_WAIT = get_float("EXPLICIT_WAIT", 20)
    POLL_FREQUENCY = get_float("POLL_FREQUENCY", 0.3)
    COMMAND_RETRY = get_int("COMMAND_RETRY", 2)

    SCREENSHOT_ON_FAILURE = get_bool("SCREENSHOT_ON_FAILURE", True)
    VIDEO_ON_FAILURE = get_bool("VIDEO_ON_FAILURE", False)
    SCREENSHOT_DIR = ROOT_DIR / get("SCREENSHOT_DIR", "reports/screenshots")
    ARTIFACT_DIR = ROOT_DIR / get("ARTIFACT_DIR", "artifacts")
    REPORT_DIR = ROOT_DIR / get("REPORT_DIR", "reports")

    STEP_REPORT = get_bool("STEP_REPORT", True)
    KEEP_EVIDENCE = get_bool("KEEP_EVIDENCE", False)
    STEP_PRINT = get_bool("STEP_PRINT", True)
    STEP_SCREENSHOTS = get_bool("STEP_SCREENSHOTS", False)
    STEP_CAPTURE_SCREENSHOTS = get_bool("STEP_CAPTURE_SCREENSHOTS", True)
    PDF_REPORT = get_bool("PDF_REPORT", True)
    SORT_TESTS = get_bool("SORT_TESTS", True)
    TEST_ORDER = get("TEST_ORDER", "")
    TEST_DATA_FILE = get("TEST_DATA_FILE", "test_data/swing_ios_test_data.xlsx")

    TEST_USERNAME = get("TEST_USERNAME")
    TEST_PASSWORD = get("TEST_PASSWORD")
    TEST_PHONE_NUMBER = get("TEST_PHONE_NUMBER")
    TEST_COUNTRY = get("TEST_COUNTRY", "ID (+62)")
    TEST_COUNTRY_NAME = get("TEST_COUNTRY_NAME", "Indonesia")

    @classmethod
    def server_url(cls):
        override = get("APPIUM_BASE_URL")
        if override:
            return override.rstrip("/")
        path = cls.APPIUM_PATH.strip("/") if cls.APPIUM_PATH else ""
        base = f"http://{cls.APPIUM_HOST}:{cls.APPIUM_PORT}"
        return f"{base}/{path}" if path else base

    @classmethod
    def app_reset_strategy(cls):
        return get("APP_RESET_STRATEGY", cls.APP_RESET_STRATEGY).lower()

    @classmethod
    def is_real_device(cls):
        return cls.TARGET == "real_device"


settings = Settings()
