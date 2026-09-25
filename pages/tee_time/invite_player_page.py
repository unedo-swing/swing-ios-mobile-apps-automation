from locators.tee_time.invite_player_locators import InvitePlayerLocators as L
from pages.base_page import BasePage


class InvitePlayerPage(BasePage):
    ROOT_LOCATOR = L.EL_TITLE
    PAGE_NAME = "InvitePlayerPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_TITLE, timeout=20), "Invite a player sheet not shown"
        assert self.is_visible(L.EL_SEARCH_BAR, timeout=5), "Invite a player search bar not shown"
        assert self.is_visible(L.INPUT_SEARCH, timeout=5), "Invite a player search field not shown"
        assert self.is_visible(L.BTN_CLOSE, timeout=5), "Invite a player close button not shown"
        self.capture_step("invite_player")
        return self

    def search_friend(self, text):
        self.capture_step("search_friend")
        self.type(L.INPUT_SEARCH, text)

    def submit_search(self):
        self.capture_step("submit_search")
        self.click(L.BTN_KEYBOARD_SEARCH)

    def select_friend(self, name):
        self.capture_step("select_friend")
        self.click(L.TXT_FRIEND_BY_NAME.format(name))

    def tap_confirm(self):
        self.capture_step("tap_confirm")
        self.click(L.BTN_CONFIRM)

    def tap_close(self):
        self.capture_step("tap_close")
        self.click(L.BTN_CLOSE)

    def search_hint_text(self):
        return self.label_of(L.TXT_SEARCH_HINT)

    def result_count_text(self):
        return self.label_of(L.TXT_RESULT_COUNT)

    def friend_text(self, name):
        return self.label_of(L.TXT_FRIEND_BY_NAME.format(name))

    def has_friend(self, name, timeout=5):
        return self.is_visible(L.TXT_FRIEND_BY_NAME.format(name), timeout)

    def is_closed(self, timeout=10):
        return self.wait_gone(L.EL_TITLE, timeout)

    def confirm_is_enabled(self):
        return self.is_enabled(L.BTN_CONFIRM)
