import pytest

from helpers.pdf_report import init_pdf
from test_data.login_test_data import LoginTestData as D
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow


class TestRegressionV52Login:

    def _request_otp(self, login_flow: LoginFlow):
        login_flow.open_login()
        login_flow.choose_country(D.COUNTRY_NAME)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.continue_log_in()
        login_flow.choose_verification_method(D.METHOD_VERIFICATION)
        login_flow.verify_page_code_otp()

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION)
        home_flow.skip_first_run_screens(D.SPORT_TYPE)
        home_flow.verify_home()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_001"])
    def test_login_page_displayed_when_opening_app(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.open_login()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_002", "TC_DR_003", "TC_DR_004"])
    def test_request_otp_with_valid_phone_number(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_005", "TC_DR_006", "TC_DR_011"])
    def test_login_with_valid_otp_shows_choose_sport(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)
        login_flow.enter_otp_code(D.OTP, D.COUNTRY_NAME, D.PHONE_NUMBER)
        home_flow.verify_sport_option_page()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_007"])
    def test_login_with_invalid_otp_stays_on_verification(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)
        login_flow.enter_invalid_otp(D.OTP)
        login_flow.verify_page_code_otp()

    @pytest.mark.skip(reason="needs locators: expired OTP error message on Verification Code page")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_008"])
    def test_login_with_expired_otp(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_009"])
    def test_request_otp_with_invalid_phone_number(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        login_flow.open_login()
        login_flow.choose_country(D.COUNTRY_NAME)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.verify_button_continue_disabled()

    @pytest.mark.skip(reason="needs locators: resend OTP countdown and enabled state on Verification Code page")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_010"])
    def test_resend_otp_after_countdown(self, TC_ID, login_flow: LoginFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_012", "TC_DR_013"])
    def test_choose_golf_lands_on_golf_homepage(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._request_otp(login_flow)
        login_flow.enter_otp_code(D.OTP, D.COUNTRY_NAME, D.PHONE_NUMBER)
        home_flow.verify_sport_option_page()
        home_flow.select_sport(D.SPORT_TYPE)
        home_flow.enable_notifications_if_shown()
        home_flow.enable_location_if_shown()
        home_flow.dismiss_coachmark_if_shown()
        home_flow.close_whats_new_if_shown()
        home_flow.verify_home()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_014"])
    def test_stays_logged_in_after_reopening_app(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        home_flow.restart_app()
        home_flow.close_whats_new_if_shown()
        home_flow.verify_home()
