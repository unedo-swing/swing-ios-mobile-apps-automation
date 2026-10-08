from flows.base_flow import BaseFlow
from pages.homepage.notification_permission_page import NotificationPermissionPage
from pages.homepage.location_permission_page import LocationPermissionPage
from pages.homepage.coachmark_page import CoachmarkPage
from pages.homepage.whats_new_page import WhatsNewPage
from pages.homepage.home_page import HomePage
from pages.sport_option_page import SportOptionPage


class HomeFlow(BaseFlow):
    FLOW_NAME = "HomeFlow"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.notification = self.page(NotificationPermissionPage)
        self.location = self.page(LocationPermissionPage)
        self.coachmark = self.page(CoachmarkPage)
        self.whats_new = self.page(WhatsNewPage)
        self.home = self.page(HomePage)
        self.sport = self.page(SportOptionPage)
    
    def verify_sport_option_page(self):
        self.sport.verify_screen()
    
    def select_sport(self, sport: str):
        self.sport.select_sport_by_label(sport)
    
    def enable_notifications(self):
        self.notification.verify_screen()
        self.notification.tap_enable()
        self.handle_system_alerts()

    def enable_location(self):
        self.location.verify_screen()
        self.location.tap_enable()
        self.handle_system_alerts()

    def dismiss_coachmark(self):
        self.coachmark.verify_sequence()

    def close_whats_new(self):
        self.whats_new.tap_back()
        self.home.verify_screen()

    def select_sport_if_shown(self, sport, timeout=5):
        if self.sport.is_loaded(timeout):
            self.sport.select_sport_by_label(sport)

    def enable_notifications_if_shown(self, timeout=5):
        if self.notification.is_loaded(timeout):
            self.notification.tap_enable()
            self.handle_system_alerts()

    def enable_location_if_shown(self, timeout=5):
        if self.location.is_loaded(timeout):
            self.location.tap_enable()
            self.handle_system_alerts()

    def dismiss_coachmark_if_shown(self, timeout=5):
        if self.coachmark.is_loaded(timeout):
            self.coachmark.verify_sequence()

    def close_whats_new_if_shown(self, timeout=5):
        if self.whats_new.is_loaded(timeout):
            self.whats_new.tap_back()

    def skip_first_run_screens(self, sport="Golf", timeout=5):
        self.select_sport_if_shown(sport, timeout)
        self.enable_notifications_if_shown(timeout)
        self.enable_location_if_shown(timeout)
        self.dismiss_coachmark_if_shown(timeout)
        self.close_whats_new_if_shown(timeout)

    def verify_home(self):
        self.home.verify_screen()
    
    def verify_home_my(self):
        self.home.verify_screen_my()

    def open_sport_option(self):
        self.home.open_sport_option()
        self.sport.verify_screen()

    REGION_COUNTRIES = {"ID": "Indonesia", "MY": "Malaysia"}

    def open_region_picker(self):
        self.home.open_region_picker()
        assert self.home.has_region_picker(), "Select country sheet not shown"

    def select_region(self, region):
        code = str(region).strip().upper()
        self.open_region_picker()
        self.home.select_region_country(self.REGION_COUNTRIES.get(code, region))
        self.verify_region(code)

    def verify_region(self, region):
        self.home.wait_until_loaded()
        code = str(region).strip().upper()
        actual = (self.home.selected_country() or "").strip().upper()
        assert actual == code, f"home region is {actual!r} after choosing {code!r}"
