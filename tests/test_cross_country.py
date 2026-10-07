import pytest

from flows.driving_range_flow import DrivingRangeFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.tee_time_flow import TeeTimeFlow
from helpers.pdf_report import init_pdf
from test_data.driving_range_test_data import DrivingRangeTestData as DR
from test_data.player_data import load_players
from test_data.tee_time_test_data import TeeTimeTestData as TT


def login_and_switch_region(D, login_flow: LoginFlow, home_flow: HomeFlow):
    login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)
    home_flow.skip_first_run_screens(D.SPORT_TYPE)
    home_flow.verify_home()
    if D.LOGIN_REGION:
        home_flow.verify_region(D.LOGIN_REGION)
    home_flow.select_region(D.REGION)


class TestDrivingRangeCrossCountry:

    def _open_booking(self, driving_range_flow: DrivingRangeFlow):
        driving_range_flow.open_driving_range(DR.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(DR.SEARCH_KEYWORD)
        driving_range_flow.open_result(DR.VENUE)
        driving_range_flow.open_calendar()
        driving_range_flow.choose_date(DR.BOOKING_DATE)
        driving_range_flow.choose_bay_type(DR.BAY_TYPE)
        driving_range_flow.choose_time(DR.BOOKING_START_TIME, DR.BOOKING_END_TIME)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(DR.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()
        driving_range_flow.remove_promo()

    def _pay(self, driving_range_flow: DrivingRangeFlow, used_credit="0"):
        if DR.PAYMENT_TYPE == "Credit card":
            driving_range_flow.link_new_credit_card(DR.PLAYER_NAME, DR.CARD_NUMBER, DR.CARD_EXPIRY, DR.CARD_CVV, DR.CARD_OTP)
            payment_information = driving_range_flow.get_payment_information_before_payment(used_credit)
            driving_range_flow.pay_now_with_credit_card(DR.CARD_CVV, DR.CARD_OTP)
            return payment_information
        driving_range_flow.choose_payment_method(DR.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(used_credit)
        driving_range_flow.pay_now()
        driving_range_flow.simulate_gateway_payment(DR.PAYMENT_METHOD, DR.PAYMENT_TYPE)
        return payment_information

    def _verify_success(self, driving_range_flow: DrivingRangeFlow, payment_information):
        driving_range_flow.verify_payment_success_driving_range(DR.PLAYER_NAME, DR.BOOKING_DATE, DR.BOOKING_START_TIME, DR.BOOKING_END_TIME, DR.NUMBER_OF_BAYS, payment_information, DR.BAY_TYPE)
        booking_code = driving_range_flow.get_booking_code_after_payment()
        driving_range_flow.open_booking_details()
        return booking_code or ""

    @pytest.mark.app_reset("clear")
    @pytest.mark.cross_country
    @pytest.mark.parametrize("TC_ID", ["DR_CC_MY_ID_001", "DR_CC_MY_ID_002", "DR_CC_MY_ID_003", "DR_CC_MY_ID_004", "DR_CC_MY_ID_005", "DR_CC_MY_ID_006", "DR_CC_MY_ID_007", "DR_CC_MY_ID_008", "DR_CC_MY_ID_009", "DR_CC_MY_ID_010", "DR_CC_MY_ID_011", "DR_CC_MY_ID_012", "DR_CC_MY_ID_013", "DR_CC_MY_ID_014"])
    def test_cross_country_my_to_id_book_driving_range_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        DR.load(TC_ID)
        pdf = init_pdf(DR.TC_NAME, tc_id=TC_ID)
        login_and_switch_region(DR, login_flow, home_flow)
        self._open_booking(driving_range_flow)
        payment_information = self._pay(driving_range_flow)
        booking_code = self._verify_success(driving_range_flow, payment_information)
        driving_range_flow.verify_data_booking_details_without_credit_used(booking_code, DR.PLAYER_NAME, DR.BOOKING_DATE, DR.BOOKING_START_TIME, DR.BOOKING_END_TIME, DR.NUMBER_OF_BAYS, payment_information, DR.BAY_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.cross_country
    @pytest.mark.parametrize("TC_ID", ["DR_CC_002"])
    def test_cross_country_my_to_id_book_driving_range_with_swing_credits(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        DR.load(TC_ID)
        pdf = init_pdf(DR.TC_NAME, tc_id=TC_ID)
        login_and_switch_region(DR, login_flow, home_flow)
        self._open_booking(driving_range_flow)
        driving_range_flow.use_swing_credits()
        payment_information = self._pay(driving_range_flow, "1")
        booking_code = self._verify_success(driving_range_flow, payment_information)
        driving_range_flow.verify_data_booking_details_with_credit_used(booking_code, DR.PLAYER_NAME, DR.BOOKING_DATE, DR.BOOKING_START_TIME, DR.BOOKING_END_TIME, DR.NUMBER_OF_BAYS, payment_information, DR.BAY_TYPE)
        driving_range_flow.back_to_activity()
        driving_range_flow.open_home_tab()
        driving_range_flow.open_swing_credits()
        driving_range_flow.open_swing_credit_history()
        driving_range_flow.verify_used_credit_booking_code(booking_code, payment_information["used_credit"])


class TestTeeTimeCrossCountry:

    def _open_booking(self, tee_time_flow: TeeTimeFlow):
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(TT.SEARCH_KEYWORD)
        tee_time_flow.open_result(TT.VENUE)
        tee_time_flow.choose_date(TT.BOOKING_DATE)
        tee_time_flow.choose_session(TT.SESSION)
        tee_time_flow.choose_tee_time(TT.PREFERRED_TIME)
        tee_time_flow.book_tee_time()
        tee_time_flow.choose_standard_booking()
        tee_time_flow.remove_promo(TT.HOST_NAME)

    def _pay(self, tee_time_flow: TeeTimeFlow, PLAYERS, used_credit="0"):
        if TT.PAYMENT_TYPE == "Credit card":
            tee_time_flow.link_new_credit_card(TT.HOST_NAME, TT.CARD_NUMBER, TT.CARD_EXPIRY, TT.CARD_CVV, TT.CARD_OTP)
            payment_information = tee_time_flow.get_payment_information_before_payment(used_credit, PLAYERS, TT.HOST_NAME)
            tee_time_flow.pay_now_with_credit_card(TT.CARD_CVV, TT.CARD_OTP)
            return payment_information
        tee_time_flow.choose_payment_method(TT.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment(used_credit, PLAYERS, TT.HOST_NAME)
        tee_time_flow.pay_now()
        tee_time_flow.simulate_gateway_payment(TT.PAYMENT_METHOD, TT.PAYMENT_TYPE)
        return payment_information

    def _verify_success(self, tee_time_flow: TeeTimeFlow, PLAYERS, payment_information):
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, TT.HOST_NAME)
        booking_code = tee_time_flow.get_booking_code_after_payment()
        payment_method = "" if TT.PAYMENT_TYPE == "Credit card" else TT.PAYMENT_METHOD
        tee_time_flow.verify_payment_success_players(TT.BOOKING_DATE, TT.SESSION, TT.PREFERRED_TIME, payment_information, PLAYERS, TT.VENUE, payment_method)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, TT.BOOKING_DATE, TT.SESSION, TT.PREFERRED_TIME, payment_information, PLAYERS)
        return booking_code or ""

    @pytest.mark.app_reset("clear")
    @pytest.mark.cross_country
    @pytest.mark.parametrize("TC_ID", ["TT_CC_MY_ID_001", "TT_CC_MY_ID_002", "TT_CC_MY_ID_003", "TT_CC_MY_ID_004", "TT_CC_MY_ID_005", "TT_CC_MY_ID_006", "TT_CC_MY_ID_007", "TT_CC_MY_ID_008", "TT_CC_MY_ID_009", "TT_CC_MY_ID_010", "TT_CC_MY_ID_011", "TT_CC_MY_ID_012", "TT_CC_MY_ID_013", "TT_CC_MY_ID_014"])
    def test_cross_country_my_to_id_book_tee_time_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        TT.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(TT.TC_NAME, tc_id=TC_ID)
        login_and_switch_region(TT, login_flow, home_flow)
        self._open_booking(tee_time_flow)
        tee_time_flow.verify_booking_confirmation(TT.BOOKING_DATE, TT.SESSION, TT.PREFERRED_TIME, TT.BOOKING_METHOD, TT.TOTAL_PLAYERS)
        payment_information = self._pay(tee_time_flow, PLAYERS)
        self._verify_success(tee_time_flow, PLAYERS, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.cross_country
    @pytest.mark.parametrize("TC_ID", ["TT_CC_002"])
    def test_cross_country_my_to_id_book_tee_time_with_swing_credits(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        TT.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(TT.TC_NAME, tc_id=TC_ID)
        login_and_switch_region(TT, login_flow, home_flow)
        self._open_booking(tee_time_flow)
        tee_time_flow.use_swing_credits(TT.HOST_NAME)
        tee_time_flow.verify_booking_confirmation(TT.BOOKING_DATE, TT.SESSION, TT.PREFERRED_TIME, TT.BOOKING_METHOD, TT.TOTAL_PLAYERS)
        payment_information = self._pay(tee_time_flow, PLAYERS, "1")
        tee_time_flow.verify_players_used_credits(payment_information, PLAYERS, TT.HOST_NAME)
        booking_code = self._verify_success(tee_time_flow, PLAYERS, payment_information)
        tee_time_flow.back_to_activity()
        tee_time_flow.open_home_tab()
        tee_time_flow.open_swing_credits()
        tee_time_flow.open_swing_credit_history()
        tee_time_flow.verify_used_credit_booking_code_players(booking_code, payment_information, PLAYERS, TT.HOST_NAME)
