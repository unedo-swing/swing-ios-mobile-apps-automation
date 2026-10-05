from locators.payment_gateway_locators import PaymentGatewayLocators as L
from pages.base_page import BasePage


class PaymentGatewayPage(BasePage):
    ROOT_LOCATOR = L.BTN_PROCEED_TO_PAY
    PAGE_NAME = "PaymentGatewayPage"
    GATEWAY_TIMEOUT = 5

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.BTN_PROCEED_TO_PAY, timeout=20), "Payment gateway screen not shown"
        assert self.is_visible(L.IMG_XENDIT_LOGO, timeout=5), "Payment gateway provider logo not shown"
        self.capture_step("payment_gateway")
        return self

    def tap_proceed_to_pay(self):
        if not self.has_proceed_to_pay():
            return
        self.capture_step("tap_proceed_to_pay")
        self.click(L.BTN_PROCEED_TO_PAY)

    def has_proceed_to_pay(self, timeout=10):
        return self.is_visible(L.BTN_PROCEED_TO_PAY, timeout or self.GATEWAY_TIMEOUT)

    def header_text(self, method):
        return self.label_of(L.EL_HEADER_BY_METHOD.format(method))
