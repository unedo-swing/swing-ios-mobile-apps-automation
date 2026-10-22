import pytest

from helpers.pdf_report import init_pdf
from test_data.player_data import load_players
from test_data.tee_time_test_data import TeeTimeTestData as D
from flows.cancellation_flow import CancellationFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.tee_time_flow import TeeTimeFlow


class TestRegressionV52TeeTime:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)
        home_flow.skip_first_run_screens(D.SPORT_TYPE)
        home_flow.verify_home()

    def _open_details(self, tee_time_flow: TeeTimeFlow):
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)

    def _choose_tee_time(self, tee_time_flow: TeeTimeFlow):
        tee_time_flow.choose_date(D.BOOKING_DATE)
        tee_time_flow.choose_session(D.SESSION)
        tee_time_flow.choose_tee_time(D.PREFERRED_TIME)

    def _open_standard_booking(self, tee_time_flow: TeeTimeFlow):
        self._open_details(tee_time_flow)
        self._choose_tee_time(tee_time_flow)
        tee_time_flow.book_tee_time()
        tee_time_flow.choose_standard_booking()

    def _pay(self, tee_time_flow: TeeTimeFlow, PLAYERS):
        if D.PAYMENT_TYPE == "Credit card":
            tee_time_flow.link_new_credit_card(D.HOST_NAME, D.CARD_NUMBER, D.CARD_EXPIRY, D.CARD_CVV, D.CARD_OTP)
            payment_information = tee_time_flow.get_payment_information_before_payment("0", PLAYERS, D.HOST_NAME)
            tee_time_flow.pay_now_with_credit_card(D.CARD_CVV, D.CARD_OTP)
            return payment_information
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("0", PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        tee_time_flow.simulate_gateway_payment(D.PAYMENT_METHOD, D.PAYMENT_TYPE)
        return payment_information

    def _verify_booking(self, tee_time_flow: TeeTimeFlow, PLAYERS, payment_information):
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        booking_code = tee_time_flow.get_booking_code_after_payment()
        payment_method = "" if D.PAYMENT_TYPE == "Credit card" else D.PAYMENT_METHOD
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, payment_method)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)
        return booking_code

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_001", "TC_TT_002"])
    def test_open_explore_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_003"])
    def test_search_golf_course_with_valid_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.verify_search_result(D.VENUE)

    @pytest.mark.skip(reason="needs locators: empty state / no result message on Tee Time search")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_004"])
    def test_search_golf_course_with_unknown_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)
        tee_time_flow.open_search()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_005"])
    def test_clear_golf_course_search_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.clear_search()
        tee_time_flow.verify_search_cleared()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_006", "TC_TT_007"])
    def test_open_golf_course_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)
        tee_time_flow.see_all_details_sections()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_008"])
    def test_choose_tee_time_date(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)
        tee_time_flow.choose_date(D.BOOKING_DATE)
        tee_time_flow.choose_session(D.SESSION)

    @pytest.mark.skip(reason="needs locators: disabled past date state on Golf Course Details date picker")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_009"])
    def test_cannot_choose_past_date_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)

    @pytest.mark.skip(reason="needs locators: Publish Rate label, price and inclusions on Golf Course Details slot")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_010"])
    def test_verify_publish_rate_information(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_011"])
    def test_choose_publish_rate(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)
        self._choose_tee_time(tee_time_flow)
        tee_time_flow.verify_book_tee_time_enabled()

    @pytest.mark.skip(reason="needs locators: unavailable / fully booked tee time state on Golf Course Details")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_012"])
    def test_cannot_choose_unavailable_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_013"])
    def test_book_tee_time_disabled_without_rate(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(tee_time_flow)
        tee_time_flow.verify_book_tee_time_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_014", "TC_TT_015"])
    def test_book_tee_time_opens_booking_confirmation(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_016"])
    def test_promo_auto_applied_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_017"])
    def test_no_promo_applied_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_promo_removed(D.HOST_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_018"])
    def test_remove_auto_applied_promo_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.remove_promo_and_verify(D.HOST_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_019"])
    def test_choose_tee_time_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_020"])
    def test_cannot_pay_tee_time_without_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_pay_now_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_021", "TC_TT_022", "TC_TT_023"])
    def test_pay_tee_time_and_see_booking_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        payment_information = self._pay(tee_time_flow, PLAYERS)
        self._verify_booking(tee_time_flow, PLAYERS, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_024"])
    def test_tee_time_booking_appears_in_activity(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow, cancellation_flow: CancellationFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        payment_information = self._pay(tee_time_flow, PLAYERS)
        booking_code = self._verify_booking(tee_time_flow, PLAYERS, payment_information)
        tee_time_flow.back_to_activity()
        tee_time_flow.open_home_tab()
        cancellation_flow.open_activity()
        cancellation_flow.find_activity_card(D.VENUE)
        cancellation_flow.open_activity_card(D.VENUE)
        cancellation_flow.verify_booking_details(booking_code)

    @pytest.mark.skip(reason="needs locators: booked tee time unavailable / reduced slot state on Golf Course Details")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_025"])
    def test_booked_tee_time_no_longer_available(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_TT_026", "TC_TT_027", "TC_TT_028", "TC_TT_029", "TC_TT_030", "TC_TT_031", "TC_TT_032", "TC_TT_033", "TC_TT_034", "TC_TT_035", "TC_TT_036", "TC_TT_037", "TC_TT_038", "TC_TT_039"])
    def test_end_to_end_standard_booking_tee_time_with_auto_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        payment_information = self._pay(tee_time_flow, PLAYERS)
        self._verify_booking(tee_time_flow, PLAYERS, payment_information)
