from locators.event.registration_method_locators import RegistrationMethodLocators as L
from pages.base_page import BasePage


class RegistrationMethodPage(BasePage):
    ROOT_LOCATOR = L.TXT_TITLE
    PAGE_NAME = "RegistrationMethodPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_TITLE, timeout=20), "Registration method sheet not shown"
        # assert self.is_visible(L.EL_GROUP_REGISTRATION, timeout=5), "Registration method group option not shown"
        assert self.is_visible(L.EL_STANDARD_REGISTRATION, timeout=5), "Registration method standard option not shown"
        assert self.is_visible(L.BTN_LEARN_MORE, timeout=5), "Registration method learn more button not shown"
        self.capture_step("registration_method")
        return self

    def choose_group_registration(self):
        self.capture_step("choose_group_registration")
        self.click(L.EL_GROUP_REGISTRATION)

    def choose_standard_registration(self):
        self.capture_step("choose_standard_registration")
        self.click(L.EL_STANDARD_REGISTRATION)

    def choose_method(self, name):
        self.capture_step("choose_method")
        self.click(L.EL_METHOD_BY_NAME.format(name))

    def open_learn_more(self):
        self.capture_step("open_learn_more")
        self.click(L.BTN_LEARN_MORE)

    def tap_close(self):
        self.capture_step("tap_close")
        self.click(L.BTN_CLOSE)

    def title_text(self):
        return self.label_of(L.TXT_TITLE)

    def group_registration_text(self):
        return self.label_of(L.EL_GROUP_REGISTRATION)

    def standard_registration_text(self):
        return self.label_of(L.EL_STANDARD_REGISTRATION)

    def has_method(self, name, timeout=5):
        return self.is_visible(L.EL_METHOD_BY_NAME.format(name), timeout)
