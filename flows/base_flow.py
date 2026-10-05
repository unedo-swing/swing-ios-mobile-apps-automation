from typing import TypeVar, cast

from config.settings import settings
from helpers import alerts, app_helper, device, gestures, media, waits
from helpers.logger import get_logger
from helpers.reporter import reporter as default_reporter
from pages.base_page import BasePage

PageT = TypeVar("PageT", bound=BasePage)


class BaseFlow:
    FLOW_NAME = "BaseFlow"

    def __init__(self, driver, reporter=None):
        self.driver = driver
        self.settings = settings
        self.reporter = reporter or default_reporter
        self.log = get_logger(self.__class__.__name__)
        self._pages: dict[str, BasePage] = {}

    def page(self, page_class: type[PageT]) -> PageT:
        key = page_class.__name__
        if key not in self._pages:
            self._pages[key] = page_class(self.driver)
        return cast(PageT, self._pages[key])

    def invited_players(self, players):
        return [player for player in players or []
                if isinstance(player, dict) and str(player.get("add_method", "")).lower() != "host"]

    def player_number(self, total_players):
        text = str(total_players).strip()
        return int(text) if text.isdigit() else 0

    def players_to_invite(self, players, total_players=""):
        invited = self.invited_players(players)
        if not str(total_players).strip().isdigit():
            return invited
        limit = max(int(total_players) - 1, 0)
        assert limit <= len(invited), (
            f"the booking is set to {total_players} players so {limit} have to be invited, "
            f"but the player data only has {len(invited)}")
        return invited[:limit]

    def player_total(self, players, total_players=""):
        return 1 + len(self.players_to_invite(players, total_players))

    def player_names(self, players):
        if not players:
            return []
        if isinstance(players, str):
            return [players]
        if isinstance(players, dict):
            return [players["player"]]
        return [player["player"] if isinstance(player, dict) else str(player) for player in players]

    def payment_player_names(self, players=None, host="", total_players=""):
        invited = self.players_to_invite(players, total_players) if total_players else players
        names = ([host] if host else []) + self.player_names(invited)
        return list(dict.fromkeys(name for name in names if name))

    SIMULATED_PAYMENT_TYPES = ("qris", "virtual account")

    def simulate_gateway_payment(self, payment_method, payment_type):
        kind = str(payment_type or "").strip().lower()
        if kind not in self.SIMULATED_PAYMENT_TYPES:
            return None
        from helpers.api_client import ApiClient
        from helpers.db_queries import pending_booking_payment

        payment = pending_booking_payment(payment_method)
        client = ApiClient.swing()
        if kind == "qris":
            response = client.simulate_qr_payment(payment["id"])
        else:
            response = client.simulate_va_payment(payment["id"], payment["value"])
        self.log.info(f"simulated {payment['payment_method']} payment order {payment['id']} "
                      f"amount {payment['value']}: HTTP {response.status} {response.text[:300]}")
        self.step(f"Simulate {payment['payment_method']} payment, order {payment['id']}")
        response.raise_for_status()
        return payment["id"]

    def step(self, description):
        self.reporter.step(description)
        return self

    def restart_app(self):
        app_helper.restart(self.driver)
        return self

    def terminate_app(self):
        app_helper.terminate(self.driver)
        return self

    def activate_app(self):
        app_helper.activate(self.driver)
        return self

    def background_app(self, seconds=5):
        device.background_app(self.driver, seconds)
        return self

    def open_deeplink(self, url):
        device.open_deeplink(self.driver, url, app_helper.bundle_of(self.driver))
        return self

    def handle_system_alerts(self, accept=True, max_alerts=3):
        alerts.handle_all(self.driver, accept, max_alerts)
        return self

    def swipe(self, direction="up"):
        gestures.swipe(self.driver, direction)
        return self

    def wait_for(self, condition, timeout=None, message="flow condition failed"):
        waits.wait_until_true(condition, timeout, message=message)
        return self

    def screenshot(self, name=None):
        path = media.screenshot(self.driver, name or self.FLOW_NAME)
        self.reporter.attach(path, name or self.FLOW_NAME)
        return path
