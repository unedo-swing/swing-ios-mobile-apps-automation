from locators.confirm_credit_card_locators import ConfirmCreditCardLocators as L
from pages.base_page import BasePage


class ConfirmCreditCardPage(BasePage):
    ROOT_LOCATOR = L.TXT_TITLE
    PAGE_NAME = "ConfirmCreditCardPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_TITLE, timeout=20), "Confirm your credit card screen not shown"
        assert self.is_visible(L.TXT_SECURITY_NOTE, timeout=5), "Confirm credit card security note not shown"
        assert self.is_visible(L.INPUT_CVV, timeout=5), "CVV field not shown"
        assert self.is_visible(L.BTN_CONFIRM, timeout=5), "Confirm button not shown"
        self.capture_step("confirm_credit_card")
        return self

    def enter_cvv(self, cvv):
        self.capture_step("enter_cvv", cvv)
        self.type(L.INPUT_CVV, cvv)
        self.hide_keyboard()
    
    def enter_cvv_card(self, cvv):
        self.capture_step("enter_cvv", cvv)
        self.type(L.INPUT_CVV_BY_CARD, cvv)
        self.hide_keyboard()

    def clear_cvv(self):
        self.capture_step("clear_cvv")
        self.clear(L.INPUT_CVV)

    def tap_cvv_info(self):
        self.capture_step("tap_cvv_info")
        self.click(L.BTN_CVV_INFO)

    def tap_confirm(self):
        self.capture_step("tap_confirm")
        self.click(L.BTN_CONFIRM)

    def tap_back(self):
        self.capture_step("tap_back")
        self.click(L.BTN_BACK)

    def title_text(self):
        return self.text_of(L.TXT_TITLE)

    def security_note_text(self):
        return self.label_of(L.TXT_SECURITY_NOTE)

    def cvv_value(self):
        return self.value_of(L.INPUT_CVV)

    def has_cvv_hint_for(self, card, timeout=5):
        return self.is_visible(L.INPUT_CVV_BY_CARD.format(card), timeout)

    def confirm_is_enabled(self):
        return self.is_enabled(L.BTN_CONFIRM)
