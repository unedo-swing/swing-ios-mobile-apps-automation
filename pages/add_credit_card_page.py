from locators.add_credit_card_locators import AddCreditCardLocators as L
from pages.base_page import BasePage


class AddCreditCardPage(BasePage):
    ROOT_LOCATOR = L.EL_HEADER
    PAGE_NAME = "AddCreditCardPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_HEADER, timeout=20), "Add credit card screen not shown"
        assert self.is_visible(L.INPUT_CARDHOLDER_NAME, timeout=5), "Cardholder name field not shown"
        assert self.is_visible(L.EL_CARD_NUMBER_FIELD, timeout=5), "Card number field not shown"
        assert self.is_visible(L.INPUT_EXPIRY_DATE, timeout=5), "Expiry date field not shown"
        assert self.is_visible(L.BTN_SAVE_CREDIT_CARD, timeout=5), "Save credit card button not shown"
        self.capture_step("add_credit_card")
        return self

    def enter_cardholder_name(self, name):
        self.capture_step("Enter cardholder name", name)
        self.type(L.INPUT_CARDHOLDER_NAME, name)

    def enter_card_number(self, number):
        self.capture_step("Enter card number", number)
        self.type(L.INPUT_CARD_NUMBER, number)

    def enter_expiry_date(self, expiry):
        self.capture_step("Enter expiry date", expiry)
        self.type(L.INPUT_EXPIRY_DATE, expiry)

    def enter_cvv(self, cvv):
        self.capture_step("Enter CVV", cvv)
        self.type(L.INPUT_CVV, cvv)
        self.hide_keyboard()

    def set_primary_method(self, on=True):
        self.capture_step("Set as primary method", on)
        self.set_switch(L.SWITCH_PRIMARY_METHOD, on)

    def toggle_primary_method(self):
        self.capture_step("Toggle primary method")
        self.click(L.SWITCH_PRIMARY_METHOD)

    def open_terms(self):
        self.capture_step("Open terms and conditions")
        self.click(L.LINK_TERMS)

    def tap_save_credit_card(self):
        self.capture_step("Save credit card")
        self.click(L.BTN_SAVE_CREDIT_CARD)

    def tap_back(self):
        self.capture_step("Back from add credit card")
        self.click(L.BTN_BACK)

    def cardholder_name_value(self):
        return self.value_of(L.INPUT_CARDHOLDER_NAME)

    def card_number_value(self):
        return self.value_of(L.INPUT_CARD_NUMBER)

    def expiry_date_value(self):
        return self.value_of(L.INPUT_EXPIRY_DATE)

    def cvv_value(self):
        return self.value_of(L.INPUT_CVV)

    def charge_note_text(self):
        return self.label_of(L.TXT_CHARGE_NOTE)

    def terms_note_text(self):
        return self.label_of(L.TXT_TERMS_NOTE)

    def has_card_brand(self, timeout=5):
        return self.is_visible(L.IMG_CARD_BRAND, timeout)

    def primary_method_is_on(self):
        return self.is_selected(L.SWITCH_PRIMARY_METHOD)

    def save_is_enabled(self):
        return self.is_enabled(L.BTN_SAVE_CREDIT_CARD)
