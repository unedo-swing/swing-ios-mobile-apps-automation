import os
import re

import pytest

from config import settings as config
from config.settings import settings
from flows.group_booking_flow import GroupBookingFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from helpers import app_helper, media
from helpers.driver_factory import create_driver, quit_driver
from helpers.logger import get_logger

log = get_logger("fixture")


def player_env(index, key):
    value = config.get(f"PLAYER_{index + 1}_{key}")
    if value is None and index == 0:
        value = getattr(settings, f"PLAYER_{key}", None)
    return value


def player_capabilities(player, index=0):
    udid = player.get("udid") or player_env(index, "UDID")
    device_name = player.get("device_name") or player_env(index, "DEVICE_NAME")
    if not (udid or device_name):
        raise ValueError(
            f"no device for {player.get('player')}: set PLAYER_{index + 1}_UDID in the env file "
            f"or Device UDID in the Players sheet")
    caps = {
        "appium:udid": udid,
        "appium:deviceId": udid,
        "appium:deviceName": device_name,
        "appium:platformVersion": player.get("platform_version") or player_env(index, "PLATFORM_VERSION"),
        "appium:wdaLocalPort": player.get("wda_port") or int(player_env(index, "WDA_LOCAL_PORT") or 0)
                               or settings.PLAYER_WDA_LOCAL_PORT + index,
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


def busy_devices(host_udid=None):
    busy = {str(host_udid): "the host device of this test"} if host_udid else {}
    if not os.getenv("PYTEST_XDIST_WORKER"):
        return busy
    for key, value in os.environ.items():
        match = re.fullmatch(r"(DEVICE|WORKER)_(\w+?)_(UDID|WDA_LOCAL_PORT|MJPEG_PORT)", key)
        if match and value:
            busy.setdefault(str(value), f"{match.group(1)}_{match.group(2)} in this parallel run")
    return busy


class PlayerDevices:
    def __init__(self, strategy=None, bundle_id=None, host_udid=None):
        self.strategy = strategy
        self.bundle_id = bundle_id
        self.host_udid = host_udid
        self.devices = []

    def check_free(self, player, caps):
        busy = busy_devices(self.host_udid)
        for name in ("appium:udid", "appium:wdaLocalPort", "appium:mjpegServerPort"):
            value = str(caps.get(name, ""))
            if value in busy:
                pytest.fail(f"group booking player {player['player']} uses {name.split(':')[1]} {value}, "
                            f"which is also used by {busy[value]}")

    def open(self, player):
        caps = player_capabilities(player, len(self.devices))
        self.check_free(player, caps)
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
    host_caps = getattr(driver, "capabilities", None) or {}
    devices = PlayerDevices(strategy, bundle_id, host_caps.get("udid") or host_caps.get("appium:udid"))
    yield devices
    devices.close_all(getattr(request.node, "test_failed", False), request.node.name)
