import pytest

from config.settings import settings
from flows.group_booking_flow import GroupBookingFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from helpers import app_helper, media
from helpers.driver_factory import create_driver, quit_driver
from helpers.logger import get_logger

log = get_logger("fixture")


def player_capabilities(player, index=0):
    first = index == 0
    udid = player.get("udid") or (settings.PLAYER_UDID if first else "")
    device_name = player.get("device_name") or (settings.PLAYER_DEVICE_NAME if first else "")
    if not (udid or device_name):
        raise ValueError(
            f"no device for {player.get('player')}: fill Device UDID in the Players sheet")
    caps = {
        "appium:udid": udid,
        "appium:deviceId": udid,
        "appium:deviceName": device_name,
        "appium:platformVersion": player.get("platform_version") or settings.PLAYER_PLATFORM_VERSION,
        "appium:wdaLocalPort": player.get("wda_port") or settings.PLAYER_WDA_LOCAL_PORT + index,
        "appium:mjpegServerPort": settings.PLAYER_MJPEG_PORT + index,
    }
    return {key: value for key, value in caps.items() if value not in (None, "", 0)}


def reset_player_app(driver, strategy=None, bundle_id=None):
    try:
        if settings.PLAYER_TARGET == "simulator" and app_helper.normalize_strategy(strategy) == "clear":
            return app_helper.clear_data(driver, bundle_id)
        return app_helper.reset(driver, strategy, bundle_id)
    except Exception as exc:
        log.warning(f"player app reset failed ({type(exc).__name__}: {exc})")
        return app_helper.activate(driver)


class PlayerDevice:
    def __init__(self, player, driver):
        self.player = player
        self.name = player["player"]
        self.driver = driver
        self.login = LoginFlow(driver)
        self.home = HomeFlow(driver)
        self.group = GroupBookingFlow(driver)


class PlayerDevices:
    def __init__(self, strategy=None, bundle_id=None):
        self.strategy = strategy
        self.bundle_id = bundle_id
        self.devices = []

    def open(self, player):
        caps = player_capabilities(player, len(self.devices))
        log.info(f"opening player device for {player['player']}: {caps}")
        driver = create_driver(caps)
        self.devices.append(PlayerDevice(player, driver))
        if self.strategy:
            reset_player_app(driver, self.strategy, self.bundle_id)
        return self.devices[-1]

    def open_all(self, players):
        return [self.open(player) for player in players]

    def close_all(self, failed=False, name="player"):
        for device in self.devices:
            if failed and settings.SCREENSHOT_ON_FAILURE:
                try:
                    media.screenshot(device.driver, f"{name}_{device.name}")
                except Exception as exc:
                    log.warning(f"player screenshot failed: {exc}")
            quit_driver(device.driver)
        self.devices = []


@pytest.fixture
def player_devices(request, driver):
    marker = request.node.get_closest_marker("app_reset")
    strategy = None
    bundle_id = None
    if marker:
        strategy = marker.args[0] if marker.args else marker.kwargs.get("strategy")
        bundle_id = marker.kwargs.get("bundle_id")
    devices = PlayerDevices(strategy, bundle_id)
    yield devices
    devices.close_all(getattr(request.node, "test_failed", False), request.node.name)
