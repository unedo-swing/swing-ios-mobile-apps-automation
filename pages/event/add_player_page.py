from locators.event.add_player_locators import EventAddPlayerLocators as L
from pages.base_page import BasePage


class EventAddPlayerPage(BasePage):
    ROOT_LOCATOR = L.EL_TITLE
    PAGE_NAME = "EventAddPlayerPage"
    AVATAR_X_RATIO = 0.12

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_TITLE, timeout=20), "Event add player sheet not shown"
        assert self.is_visible(L.EL_TAB_ROW, timeout=5), "Event add player tabs not shown"
        assert self.is_visible(L.BTN_CLOSE, timeout=5), "Event add player close button not shown"
        self.capture_step("event_add_player")
        return self

    def open_search_friend_tab(self):
        self.capture_step("open_search_friend_tab")
        self.click(L.TAB_SEARCH_FRIEND)

    def open_add_manually_tab(self):
        self.capture_step("open_add_manually_tab")
        self.click(L.TAB_ADD_MANUALLY)

    def search_friend(self, text):
        self.capture_step("search_friend")
        self.type(L.INPUT_SEARCH, text)

    def select_friend(self, username):
        self.capture_step("select_friend")
        self.tap_row_in(L.TXT_RESULT_BY_TEXT.format(username), username, x_ratio=self.AVATAR_X_RATIO)

    def enter_first_name(self, text):
        self.capture_step("enter_first_name")
        self.type(L.INPUT_FIRST_NAME, text)

    def enter_last_name(self, text):
        self.capture_step("enter_last_name")
        self.type(L.INPUT_LAST_NAME, text)

    def enter_phone_number(self, number):
        self.capture_step("enter_phone_number")
        self.type(L.INPUT_PHONE_NUMBER, number, hide_keyboard=True, dismiss_with=L.TXT_EMAIL_NOTE)

    def enter_email(self, text):
        self.capture_step("enter_email")
        self.type(L.INPUT_EMAIL, text, hide_keyboard=True, dismiss_with=L.TXT_EMAIL_NOTE)

    def open_country_picker(self):
        self.capture_step("open_country_picker")
        self.click(L.EL_COUNTRY)

    def open_contacts(self):
        self.capture_step("open_contacts")
        self.click(L.IMG_ADD_FROM_CONTACTS)

    def tap_save_player(self):
        self.capture_step("tap_save_player")
        self.scroll_and_click(L.BTN_SAVE_PLAYER)

    def tap_close(self):
        self.capture_step("tap_close")
        self.click(L.BTN_CLOSE)

    def result_text(self):
        return self.label_of(L.TXT_RESULT_COUNT)

    def selected_country(self):
        return self.value_of(L.EL_COUNTRY)

    def first_name_value(self):
        return self.value_of(L.INPUT_FIRST_NAME)

    def last_name_value(self):
        return self.value_of(L.INPUT_LAST_NAME)

    def phone_number_value(self):
        return self.value_of(L.INPUT_PHONE_NUMBER)

    def has_result(self, text, timeout=5):
        return self.is_visible(L.TXT_RESULT_BY_TEXT.format(text), timeout)

    def save_player_is_enabled(self):
        return self.is_enabled(L.BTN_SAVE_PLAYER)
