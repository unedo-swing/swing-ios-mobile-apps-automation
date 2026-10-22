import pytest

from helpers.pdf_report import init_pdf
from test_data.add_ons_data import load_add_ons
from test_data.driving_range_test_data import DrivingRangeTestData as D
from flows.driving_range_flow import DrivingRangeFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.cancellation_flow import CancellationFlow
from flows.reschedule_flow import RescheduleFlow


@pytest.mark.device(1)
class TestDrivingRangeSmoke:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)
        home_flow.skip_first_run_screens(D.SPORT_TYPE)
        home_flow.verify_home()

    def _open_booking_confirmation(self, driving_range_flow: DrivingRangeFlow):
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)
        driving_range_flow.open_calendar()
        driving_range_flow.choose_date(D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_TYPE)
        driving_range_flow.choose_time(D.BOOKING_START_TIME, D.BOOKING_END_TIME)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()

    def _pay(self, driving_range_flow: DrivingRangeFlow, used_credit="0"):
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment(used_credit)
        driving_range_flow.pay_now()
        driving_range_flow.simulate_gateway_payment(D.PAYMENT_METHOD, D.PAYMENT_TYPE)
        return payment_information

    def _verify_booking(self, driving_range_flow: DrivingRangeFlow, payment_information, used_credit=False):
        driving_range_flow.verify_payment_success_driving_range(D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.NUMBER_OF_BAYS, payment_information, D.BAY_TYPE)
        booking_code = driving_range_flow.get_booking_code_after_payment()
        driving_range_flow.open_booking_details()
        if used_credit:
            driving_range_flow.verify_data_booking_details_with_credit_used(booking_code, D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.NUMBER_OF_BAYS, payment_information, D.BAY_TYPE)
        else:
            driving_range_flow.verify_data_booking_details_without_credit_used(booking_code, D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.NUMBER_OF_BAYS, payment_information, D.BAY_TYPE)
        return booking_code

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_001", "DR_002", "DR_003"])
    def test_explore_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_004"])
    def test_result_search_driving_range_only_swing_pass(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.only_swing_pass_partners(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_005"])
    def test_result_search_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_006"])
    def test_venue_details_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)
        driving_range_flow.see_all_details_sections()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_007", "DR_008", "DR_009"])
    def test_featured_promo_swing_pass_driving_range_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)
        driving_range_flow.verify_button_exclusive_featured_promo(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_010"])
    def test_see_all_featured_promo_driving_range_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)
        driving_range_flow.open_featured_promos()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_011"])
    def test_maximum_bay_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)
        driving_range_flow.open_calendar()
        driving_range_flow.choose_date(D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_TYPE)
        driving_range_flow.choose_time(D.BOOKING_START_TIME, D.BOOKING_END_TIME)
        driving_range_flow.book_driving_range()
        driving_range_flow.verify_maximum_bays_driving_range(D.NUMBER_OF_BAYS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_012"])
    def test_booking_information_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_booking_information(D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_013"])
    def test_maximum_balls_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        ITEMS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.set_items(ITEMS)
        driving_range_flow.verify_maximum_balls()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_014"])
    def test_minimum_balls_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        ITEMS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.set_items(ITEMS)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        driving_range_flow.pay_now()
        driving_range_flow.verify_minimum_balls()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_019"])
    def test_book_with_auto_applied_promo_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_auto_applied_promo(D.PROMO_NAME)
        payment_information = self._pay(driving_range_flow)
        self._verify_booking(driving_range_flow, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_022"])
    def test_book_with_change_promo_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.apply_promo(D.PROMO_NAME)
        payment_information = self._pay(driving_range_flow)
        self._verify_booking(driving_range_flow, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_023"])
    def test_book_with_redeemed_promo_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.apply_and_redeem_promo(D.PROMO_NAME, D.PROMO_CODE)
        payment_information = self._pay(driving_range_flow)
        self._verify_booking(driving_range_flow, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_026"])
    def test_book_using_credit_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.remove_promo()
        driving_range_flow.use_swing_credits()
        payment_information = self._pay(driving_range_flow, "1")
        booking_code = self._verify_booking(driving_range_flow, payment_information, used_credit=True)
        driving_range_flow.back_to_activity()
        driving_range_flow.open_home_tab()
        driving_range_flow.open_swing_credits()
        driving_range_flow.open_swing_credit_history()
        driving_range_flow.verify_used_credit_booking_code(booking_code, payment_information["used_credit"])

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_REGRESS_EXIST_005"])
    def test_book_then_reschedule_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow, reschedule_flow: RescheduleFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.remove_promo()
        payment_information = self._pay(driving_range_flow)
        booking_code = self._verify_booking(driving_range_flow, payment_information)
        reschedule_flow.open_booking_options()
        reschedule_flow.choose_reschedule_booking()
        reschedule_flow.verify_reschedule_page()
        reschedule_flow.open_calendar()
        reschedule_flow.choose_new_date(D.RESCHEDULE_DAY)
        reschedule_flow.choose_new_time(D.RESCHEDULE_TIME)
        reschedule_flow.confirm_new_date_time()
        reschedule_flow.verify_confirm_reschedule(D.PLAYER_NAME, booking_code, D.RESCHEDULE_DURATION, D.BAY_TYPE, "", "")
        reschedule_flow.choose_reschedule_reason(D.RESCHEDULE_REASON)
        reschedule_flow.confirm_reschedule_and_pay()
        reschedule_flow.confirm_reschedule()
        reschedule_flow.verify_reschedule_success("", "", booking_code, D.VENUE)
        reschedule_flow.see_booking_details()
        reschedule_flow.verify_booking_details_after_reschedule(booking_code, "RESCHEDULED", "", D.RESCHEDULE_TIME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["DR_REGRESS_EXIST_006"])
    def test_book_then_cancel_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow, cancellation_flow: CancellationFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.remove_promo()
        payment_information = self._pay(driving_range_flow)
        booking_code = self._verify_booking(driving_range_flow, payment_information)
        cancellation_flow.open_booking_options()
        cancellation_flow.choose_cancel_booking()
        cancellation_flow.verify_cancellation_policy()
        cancellation_flow.continue_cancel()
        cancellation_flow.confirm_cancellation()
        cancellation_flow.verify_cancellation_success(booking_code, D.VENUE)
        cancellation_flow.see_booking_details()
        cancellation_flow.verify_booking_details_after_cancellation(booking_code, "CANCELLED")
