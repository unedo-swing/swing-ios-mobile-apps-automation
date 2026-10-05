from locators.payment_method_locators import PaymentMethodLocators as L
from pages.base_page import BasePage


class PaymentMethodPage(BasePage):
    ROOT_LOCATOR = L.EL_HEADER
    PAGE_NAME = "PaymentMethodPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_HEADER, timeout=20), "Payment method screen not shown"
        assert self.is_visible(L.TXT_CREDIT_CARDS, timeout=5), "Payment method credit cards section not shown"
        assert self.is_visible(L.BTN_ADD_CREDIT_CARD, timeout=5), "Payment method add credit card button not shown"
        self.capture_step("payment_method")
        return self

    def select_method(self, name):
        self.capture_step("Select method", name)
        self.scroll_to(L.IMG_METHOD_BY_NAME.format(name))
        self.click(L.IMG_METHOD_BY_NAME.format(name))

    def scroll_to_method(self, name):
        self.capture_step("scroll_to_method")
        self.scroll_to(L.IMG_METHOD_BY_NAME.format(name))

    def add_credit_card(self):
        self.capture_step("add_credit_card")
        self.click(L.BTN_ADD_CREDIT_CARD)

    def tap_back(self):
        self.capture_step("tap_back")
        self.click(L.BTN_BACK)

    def has_method(self, name, timeout=5):
        return self.is_visible(L.IMG_METHOD_BY_NAME.format(name), timeout)

    def has_section(self, name, timeout=5):
        return self.is_visible(L.TXT_SECTION_BY_NAME.format(name), timeout)

    def credit_card_count(self):
        return self.count(L.LIST_CREDIT_CARDS)
