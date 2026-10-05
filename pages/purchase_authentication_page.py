from locators.purchase_authentication_locators import PurchaseAuthenticationLocators as L
from pages.base_page import BasePage


class PurchaseAuthenticationPage(BasePage):
    ROOT_LOCATOR = L.TXT_TITLE
    PAGE_NAME = "PurchaseAuthenticationPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_TITLE, timeout=20), "Purchase authentication screen not shown"
        assert self.is_visible(L.TXT_ENTER_CODE_LABEL, timeout=5), "Enter your code label not shown"
        assert self.is_visible(L.INPUT_OTP_CODE, timeout=5), "Authentication code field not shown"
        assert self.is_visible(L.BTN_SUBMIT, timeout=5), "Submit button not shown"
        self.capture_step("purchase_authentication")
        return self

    def enter_otp_code(self, code):
        self.capture_step("enter_otp_code", code)
        self.type(L.INPUT_OTP_CODE, code)

    def hide_otp_keyboard(self):
        self.capture_step("hide_otp_keyboard")
        self.hide_keyboard()

    def double_tap_middle(self):
        self.capture_step("double_tap_middle")
        self.double_tap_center()

    def clear_otp_code(self):
        self.capture_step("clear_otp_code")
        self.clear(L.INPUT_OTP_CODE)

    def tap_submit(self):
        self.capture_step("tap_submit")
        self.click(L.BTN_SUBMIT)

    def tap_resend_code(self):
        self.capture_step("tap_resend_code")
        self.click(L.BTN_RESEND_CODE)

    def tap_cancel(self):
        self.capture_step("tap_cancel")
        self.click(L.BTN_CANCEL)

    def tap_need_help(self):
        self.capture_step("tap_need_help")
        self.click(L.TXT_NEED_HELP)

    def tap_learn_more(self):
        self.capture_step("tap_learn_more")
        self.click(L.TXT_LEARN_MORE)

    def tap_nav_cancel(self):
        self.capture_step("tap_nav_cancel")
        self.click(L.BTN_NAV_CANCEL)

    def tap_close(self):
        self.capture_step("tap_close")
        self.click(L.BTN_CLOSE)

    def tap_back(self):
        self.capture_step("tap_back")
        self.click(L.BTN_BACK)

    def title_text(self):
        return self.text_of(L.TXT_TITLE)

    def otp_message_text(self):
        return self.label_of(L.TXT_OTP_MESSAGE)

    def otp_code_value(self):
        return self.value_of(L.INPUT_OTP_CODE)

    def help_content_text(self):
        return self.label_of(L.TXT_HELP_CONTENT)

    def authentication_info_text(self):
        return self.label_of(L.TXT_AUTHENTICATION_INFO)

    def has_challenge_iframe(self, timeout=10):
        return self.is_visible(L.EL_CHALLENGE_IFRAME, timeout)

    def has_card_header(self, timeout=5):
        return self.is_visible(L.EL_HEADER_VISA, timeout)

    def has_xendit_navigation_bar(self, timeout=5):
        return self.is_visible(L.NAV_XENDIT_AUTHENTICATION, timeout)

    def submit_is_enabled(self):
        return self.is_enabled(L.BTN_SUBMIT)
