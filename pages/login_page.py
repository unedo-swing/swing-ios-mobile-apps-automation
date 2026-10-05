from locators.login_locators import LoginLocators as L
from helpers.api_client import ApiClient, ApiError, otp_code
from pages.base_page import BasePage

import time


class LoginPage(BasePage):
    ROOT_LOCATOR = L.INPUT_PHONE_NUMBER
    PAGE_NAME = "LoginPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.INPUT_PHONE_NUMBER, timeout=20), "Login screen not shown"
        assert self.is_visible(L.PICKER_COUNTRY, timeout=5), "Country selector not shown"
        assert self.is_visible(L.BTN_CONTINUE, timeout=5), "Continue button not shown"
        self.capture_step("Verify login page")
        self.wait(2)
        return self

    def select_country(self):
        self.capture_step("Tap Button Select Country")
        self.click(L.PICKER_COUNTRY)

    def selected_country(self):
        return self.value_of(L.PICKER_COUNTRY)

    def has_country(self, value, timeout=5):
        return self.is_visible(L.PICKER_COUNTRY_BY_VALUE.format(value), timeout)

    def enter_phone_number(self, number):
        self.capture_step("Enter phone number", number)
        self.type(L.INPUT_PHONE_NUMBER, number, hide_keyboard=True)

    def tap_continue(self):
        self.capture_step("Tap continue")
        self.click(L.BTN_CONTINUE)

    def continue_is_enabled(self):
        return self.is_enabled(L.BTN_CONTINUE)

    def is_loaded(self, timeout=10):
        return self.is_visible(L.EL_SCREEN_ROOT, timeout)

    
    def fetch_otp_from_api(self, phone: str = "", dial_code: str = "", method: str = "") -> str:
        time.sleep(5)
        number = str(phone).strip()
        code_prefix = str(dial_code).strip()
        response = ApiClient.swing().request_otp(
            number, code_prefix, str(method or "whatsapp").strip().upper(),
        )
        code = otp_code(response)
        self.capture_step(
            "Request OTP from API",
            f"{code_prefix or '(default dial code)'} {number} - "
            + (f"got a {len(code)}-digit code back" if code else "no code in the response"))
        return code
    
    def resolve_otp_code(self, otp: str = "", phone: str = "", dial_code: str = "") -> str:
        value = str(otp or "").strip()
        if value.casefold() in ("api", "auto"):
            code = self.fetch_otp_from_api(phone, dial_code)
            if not code:
                raise ApiError("the OTP endpoint answered without a code")
            return code
        if value:
            return value
        try:
            code = self.fetch_otp_from_api(phone, dial_code)
        except ApiError as exc:
            print(f"[otp] API call failed ({exc}) — falling back to manual entry")
            code = ""
        print(code)
        return code or input("Input Your OTP : ")
