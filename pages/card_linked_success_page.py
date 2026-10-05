from locators.card_linked_success_locators import CardLinkedSuccessLocators as L
from pages.base_page import BasePage


class CardLinkedSuccessPage(BasePage):
    ROOT_LOCATOR = L.TXT_SUCCESS_TITLE
    PAGE_NAME = "CardLinkedSuccessPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_SUCCESS_TITLE, timeout=20), "Card linked success screen not shown"
        assert self.is_visible(L.TXT_SUCCESS_MESSAGE, timeout=5), "Card linked success message not shown"
        assert self.is_visible(L.IMG_SUCCESS, timeout=5), "Card linked success icon not shown"
        assert self.is_visible(L.BTN_CLOSE, timeout=5), "Card linked success close button not shown"
        self.capture_step("card_linked_success")
        return self

    def tap_close(self):
        self.capture_step("tap_close")
        self.wait(2)
        self.click(L.BTN_CLOSE)

    def tap_refresh(self):
        self.capture_step("tap_back")
        self.click(L.BTN_REFRESH)

    def tap_go_to_home(self):
        self.capture_step("tap_go_to_home")
        self.click(L.LINK_GO_TO_HOME)

    def tap_footer_link(self, name):
        self.capture_step("tap_footer_link", name)
        self.scroll_and_click(L.LINK_BY_NAME.format(name))

    def scroll_to_footer(self):
        self.capture_step("scroll_to_footer")
        self.scroll_to(L.TXT_COMPANY)

    def success_title_text(self):
        return self.text_of(L.TXT_SUCCESS_TITLE)

    def success_message_text(self):
        return self.text_of(L.TXT_SUCCESS_MESSAGE)

    def has_success_icon(self, timeout=5):
        return self.is_visible(L.IMG_SUCCESS, timeout)

    def has_footer_link(self, name, timeout=5):
        return self.is_visible(L.LINK_BY_NAME.format(name), timeout)

    def support_email_text(self):
        return self.label_of(L.LINK_EMAIL)

    def support_phone_text(self):
        return self.label_of(L.LINK_PHONE)
