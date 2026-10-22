import pytest

from helpers.pdf_report import init_pdf
from test_data.add_ons_data import load_add_ons
from test_data.driving_range_test_data import DrivingRangeTestData as D
from flows.cancellation_flow import CancellationFlow
from flows.driving_range_flow import DrivingRangeFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow


class TestRegressionV52DrivingRange:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)
        home_flow.skip_first_run_screens(D.SPORT_TYPE)
        home_flow.verify_home()

    def _open_details(self, driving_range_flow: DrivingRangeFlow):
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.open_result(D.VENUE)

    def _choose_slot(self, driving_range_flow: DrivingRangeFlow):
        driving_range_flow.open_calendar()
        driving_range_flow.choose_date(D.BOOKING_DATE)
        driving_range_flow.choose_bay_type(D.BAY_TYPE)
        driving_range_flow.choose_time(D.BOOKING_START_TIME, D.BOOKING_END_TIME)

    def _open_booking_confirmation(self, driving_range_flow: DrivingRangeFlow):
        self._open_details(driving_range_flow)
        self._choose_slot(driving_range_flow)
        driving_range_flow.book_driving_range()
        driving_range_flow.set_bays(D.NUMBER_OF_BAYS)
        driving_range_flow.confirm_bays()

    def _pay(self, driving_range_flow: DrivingRangeFlow):
        if D.PAYMENT_TYPE == "Credit card":
            driving_range_flow.link_new_credit_card(D.PLAYER_NAME, D.CARD_NUMBER, D.CARD_EXPIRY, D.CARD_CVV, D.CARD_OTP)
            payment_information = driving_range_flow.get_payment_information_before_payment("0")
            driving_range_flow.pay_now_with_credit_card(D.CARD_CVV, D.CARD_OTP)
            return payment_information
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = driving_range_flow.get_payment_information_before_payment("0")
        driving_range_flow.pay_now()
        driving_range_flow.simulate_gateway_payment(D.PAYMENT_METHOD, D.PAYMENT_TYPE)
        return payment_information

    def _verify_booking(self, driving_range_flow: DrivingRangeFlow, payment_information):
        driving_range_flow.verify_payment_success_driving_range(D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.NUMBER_OF_BAYS, payment_information, D.BAY_TYPE)
        booking_code = driving_range_flow.get_booking_code_after_payment()
        driving_range_flow.open_booking_details()
        driving_range_flow.verify_data_booking_details_without_credit_used(booking_code, D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.NUMBER_OF_BAYS, payment_information, D.BAY_TYPE)
        return booking_code

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_015", "TC_DR_016"])
    def test_open_explore_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_017"])
    def test_search_driving_range_with_valid_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)

    @pytest.mark.skip(reason="needs locators: empty state / no result message on Driving Range search")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_018"])
    def test_search_driving_range_with_unknown_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_019"])
    def test_clear_driving_range_search_keyword(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        driving_range_flow.open_driving_range(D.MEMBER_TYPE)
        driving_range_flow.open_search()
        driving_range_flow.search_driving_range(D.SEARCH_KEYWORD)
        driving_range_flow.clear_search()
        driving_range_flow.verify_search_cleared()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_020", "TC_DR_021"])
    def test_open_driving_range_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)
        driving_range_flow.see_all_details_sections()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_022"])
    def test_choose_driving_range_booking_date(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)
        driving_range_flow.open_calendar()
        driving_range_flow.choose_date(D.BOOKING_DATE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_023"])
    def test_cannot_choose_past_date_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)
        driving_range_flow.open_calendar()
        driving_range_flow.verify_past_dates_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_024"])
    def test_choose_available_driving_range_slot(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)
        self._choose_slot(driving_range_flow)
        driving_range_flow.verify_book_enabled()

    @pytest.mark.skip(reason="needs locators: unavailable / fully booked slot state on Driving Range Details")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_025"])
    def test_cannot_choose_unavailable_driving_range_slot(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_026"])
    def test_book_driving_range_disabled_without_slot(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_details(driving_range_flow)
        driving_range_flow.verify_book_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_027", "TC_DR_028"])
    def test_book_driving_range_opens_booking_confirmation(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_booking_information(D.PLAYER_NAME, D.BOOKING_DATE, D.BOOKING_START_TIME, D.BOOKING_END_TIME, D.BAY_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_029"])
    def test_add_driving_range_add_ons(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.verify_addons(ADD_ONS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_030"])
    def test_remove_driving_range_add_ons(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.remove_addons(ADD_ONS)
        driving_range_flow.verify_addons_removed(ADD_ONS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_031"])
    def test_promo_auto_applied_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_auto_applied_promo(D.PROMO_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_032"])
    def test_no_promo_applied_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_no_promo_applied()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_033"])
    def test_remove_auto_applied_promo_driving_range(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_auto_applied_promo(D.PROMO_NAME)
        driving_range_flow.remove_promo()
        driving_range_flow.verify_no_promo_applied()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_034"])
    def test_choose_driving_range_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.choose_payment_method(D.PAYMENT_METHOD)
        driving_range_flow.verify_booking_confirmation()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_035"])
    def test_cannot_pay_driving_range_without_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.verify_pay_now_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_036", "TC_DR_037", "TC_DR_038"])
    def test_pay_driving_range_and_see_booking_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        payment_information = self._pay(driving_range_flow)
        self._verify_booking(driving_range_flow, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_039"])
    def test_driving_range_booking_appears_in_activity(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow, cancellation_flow: CancellationFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        payment_information = self._pay(driving_range_flow)
        booking_code = self._verify_booking(driving_range_flow, payment_information)
        driving_range_flow.back_to_activity()
        driving_range_flow.open_home_tab()
        cancellation_flow.open_activity()
        cancellation_flow.find_activity_card(D.VENUE)
        cancellation_flow.open_activity_card(D.VENUE)
        cancellation_flow.verify_booking_details(booking_code)

    @pytest.mark.skip(reason="needs locators: booked slot unavailable / reduced capacity state on Driving Range Details")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_040"])
    def test_booked_driving_range_slot_no_longer_available(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_DR_041", "TC_DR_042", "TC_DR_043", "TC_DR_044", "TC_DR_045", "TC_DR_046", "TC_DR_047", "TC_DR_048", "TC_DR_049", "TC_DR_050", "TC_DR_051", "TC_DR_052", "TC_DR_053", "TC_DR_054"])
    def test_end_to_end_book_driving_range_with_add_ons_and_auto_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, driving_range_flow: DrivingRangeFlow):
        D.load(TC_ID)
        ADD_ONS = load_add_ons(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_booking_confirmation(driving_range_flow)
        driving_range_flow.set_items(ADD_ONS)
        driving_range_flow.verify_auto_applied_promo(D.PROMO_NAME)
        payment_information = self._pay(driving_range_flow)
        self._verify_booking(driving_range_flow, payment_information)
