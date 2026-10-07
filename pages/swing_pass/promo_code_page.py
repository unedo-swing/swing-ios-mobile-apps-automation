from locators.swing_pass.promo_code_locators import SwingPassPromoCodeLocators as L
from pages.base_page import BasePage


class SwingPassPromoCodePage(BasePage):
    ROOT_LOCATOR = L.TXT_TITLE
    PAGE_NAME = "SwingPassPromoCodePage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_TITLE, timeout=20), "Swing Pass promo code sheet not shown"
        assert self.is_visible(L.INPUT_PROMO_CODE, timeout=5), "Swing Pass promo code field not shown"
        assert self.is_visible(L.BTN_ADD_PROMO_CODE, timeout=5), "Add Swing Pass promo code button not shown"
        self.capture_step("swing_pass_promo_code")
        return self

    def enter_promo_code(self, code):
        self.capture_step("enter_promo_code", code)
        self.type(L.INPUT_PROMO_CODE, code, hide_keyboard=True)

    def tap_add(self):
        self.capture_step("tap_add")
        self.click(L.BTN_ADD_PROMO_CODE)

    def tap_close(self):
        self.capture_step("tap_close")
        self.click(L.BTN_CLOSE)

    def promo_code_value(self):
        return self.value_of(L.INPUT_PROMO_CODE)

    def add_is_enabled(self):
        return self.is_enabled(L.BTN_ADD_PROMO_CODE)
