from locators.home_locators import HomeLocators as L
from pages.base_page import BasePage


class HomePage(BasePage):
    ROOT_LOCATOR = L.EL_SPORT_BUTTON
    PAGE_NAME = "HomePage"

    def wait_until_loaded(self, timeout=None):
        super().wait_until_loaded(timeout)
        return self.wait_all_visible(
            (L.EL_COUNTRY_BUTTON, L.IMG_DRIVING_RANGE, L.IMG_TEE_TIME, L.IMG_EVENTS,
             L.IMG_MARKETPLACE, L.TAB_HOME), timeout)

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_SPORT_BUTTON, timeout=20), "Home screen not shown"
        assert self.is_visible(L.EL_COUNTRY_BUTTON, timeout=5), "Home country button not shown"
        assert self.is_visible(L.IMG_DRIVING_RANGE, timeout=5), "Home driving range menu not shown"
        assert self.is_visible(L.IMG_TEE_TIME, timeout=5), "Home tee time menu not shown"
        assert self.is_visible(L.IMG_EVENTS, timeout=5), "Home events menu not shown"
        assert self.is_visible(L.IMG_MARKETPLACE, timeout=5), "Home marketplace menu not shown"
        assert self.is_visible(L.TAB_HOME, timeout=5), "Home tab bar not shown"
        self.capture_step("Verify home page")
        return self

    def open_sport_option(self):
        self.capture_step("open_sport_option")
        self.click(L.EL_SPORT_BUTTON)

    def open_country_picker(self):
        self.capture_step("open_country_picker")
        self.click(L.EL_COUNTRY_BUTTON)

    def selected_sport(self):
        return self.label_of(L.EL_SPORT_BUTTON)

    def open_region_picker(self):
        self.capture_step("open_region_picker")
        self.click(L.EL_COUNTRY_BUTTON)

    def has_region_picker(self, timeout=20):
        return self.is_visible(L.TXT_SELECT_COUNTRY, timeout)

    def select_region_country(self, country):
        self.capture_step("select_region_country", country)
        self.scroll_and_click(L.IMG_REGION_BY_COUNTRY.format(country))

    def close_region_picker(self):
        self.capture_step("close_region_picker")
        self.click(L.BTN_CLOSE_SELECT_COUNTRY)

    def selected_country(self):
        return self.label_of(L.EL_COUNTRY_BUTTON)

    def open_search(self):
        self.capture_step("open_search")
        self.click(L.BTN_SEARCH)

    def open_notifications(self):
        self.capture_step("open_notifications")
        self.click(L.BTN_NOTIFICATION)

    def open_category(self, name):
        self.capture_step("open_category")
        self.click(L.IMG_CATEGORY.format(name))

    def open_tee_time(self):
        self.capture_step("open_tee_time")
        self.click(L.IMG_TEE_TIME)

    def open_driving_range(self):
        self.capture_step("Open driving range")
        self.click(L.IMG_DRIVING_RANGE)

    def open_events(self):
        self.capture_step("open_events")
        self.click(L.IMG_EVENTS)

    def open_marketplace(self):
        self.capture_step("open_marketplace")
        self.click(L.IMG_MARKETPLACE)

    def membership_text(self):
        return self.label_of(L.EL_MEMBERSHIP_CARD)

    def credits_text(self):
        return self.label_of(L.EL_CREDITS_CARD)

    def open_membership(self):
        self.capture_step("open_membership")
        self.click(L.EL_MEMBERSHIP_CARD)

    def open_join_swing_pass(self):
        self.capture_step("open_join_swing_pass")
        self.scroll_and_click(L.TXT_JOIN_SWING_PASS)

    def open_swing_pass(self):
        self.capture_step("open_swing_pass")
        self.scroll_and_click(L.card_swing_pass)

    def tap_join_swing_pass(self):
        self.capture_step("tap_join_swing_pass")
        self.scroll_and_click(L.TXT_JOIN_SWING_PASS)

    def has_swing_pass(self, timeout=5):
        return self.is_visible(L.card_swing_pass, timeout)

    def has_join_swing_pass(self, timeout=5):
        return self.is_visible(L.TXT_JOIN_SWING_PASS, timeout)

    def open_credits(self):
        self.capture_step("Open credits")
        self.tap(L.EL_CREDITS_CARD)

    def updates_title_text(self):
        return self.text_of(L.TXT_UPDATES_TITLE)

    def open_banner(self, banner_id):
        self.capture_step("open_banner")
        self.click(L.IMG_BANNER_CARD.format(banner_id))

    def open_banner_by_label(self, label):
        self.capture_step("open_banner_by_label")
        self.click(L.IMG_BANNER_BY_LABEL.format(label))

    def banner_count(self):
        return self.count(L.LIST_BANNER_CARDS)

    def banner_items(self):
        return self.texts_of(L.LIST_BANNER_CARDS)

    def swipe_banners(self, direction="left"):
        self.capture_step("swipe_banners")
        self.swipe(direction, element=self.find(L.LIST_BANNER_SCROLL))

    def explore_title_text(self):
        return self.text_of(L.TXT_EXPLORE_TITLE)

    def tap_see_all(self):
        self.capture_step("tap_see_all")
        self.click(L.BTN_SEE_ALL)

    def open_explore_card(self, text):
        self.capture_step("open_explore_card")
        self.click(L.EL_EXPLORE_CARD.format(text))

    def explore_card_count(self):
        return self.count(L.LIST_EXPLORE_PRICE_CARDS)

    def open_tab(self, name):
        self.capture_step("open_tab")
        self.click(L.TAB_BY_NAME.format(name))

    def open_activity_tab(self):
        self.capture_step("open_activity_tab")
        self.click(L.TAB_ACTIVITY)
    
    def open_home_tab(self):
        self.click(L.TAB_HOME)
        self.capture_step("Open Home Tab")

    def open_account_tab(self):
        self.capture_step("open_account_tab")
        self.click(L.TAB_ACCOUNT)

    def home_tab_is_selected(self):
        return self.is_selected(L.TAB_HOME)
