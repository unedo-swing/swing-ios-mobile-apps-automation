import pytest

from helpers.pdf_report import init_pdf
from test_data.event_package import load_package
from test_data.event_test_data import EventTestData as D
from test_data.player_data import load_players
from flows.cancellation_flow import CancellationFlow
from flows.event_flow import EventFlow
from flows.event_package_flow import EventPackageFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow


class TestRegressionV52Event:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.login_with_otp(D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)
        home_flow.skip_first_run_screens(D.SPORT_TYPE)
        home_flow.verify_home()

    def _open_event(self, event_flow: EventFlow):
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)

    def _open_registration_without_package(self, event_flow: EventFlow):
        self._open_event(event_flow)
        event_flow.secure_slot()
        event_flow.choose_standard_registration()

    def _open_registration_with_package(self, event_flow: EventFlow, event_package_flow: EventPackageFlow, PACKAGES):
        self._open_event(event_flow)
        event_package_flow.secure_slot()
        event_package_flow.set_packages(PACKAGES)
        event_package_flow.confirm_packages()
        event_flow.choose_standard_registration()

    def _pay(self, event_flow: EventFlow):
        if D.PAYMENT_TYPE == "Credit card":
            event_flow.link_new_credit_card(D.CARD_NAME, D.CARD_NUMBER, D.CARD_EXPIRY, D.CARD_CVV, D.CARD_OTP)
            payment_information = event_flow.get_payment_information_before_payment("0")
            event_flow.pay_now_with_credit_card(D.CARD_CVV, D.CARD_OTP)
            return payment_information
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        event_flow.simulate_gateway_payment(D.PAYMENT_METHOD, D.PAYMENT_TYPE)
        return payment_information

    def _verify_registration(self, event_flow: EventFlow, PLAYERS, payment_information):
        registration_code = event_flow.get_registration_code_after_payment()
        payment_method = "" if D.PAYMENT_TYPE == "Credit card" else D.PAYMENT_METHOD
        event_flow.verify_payment_success_event(D.EVENT_DATE, D.STARTING_TIME, payment_information, PLAYERS, D.VENUE, payment_method, D.TOTAL_PLAYERS)
        event_flow.open_registration_details()
        event_flow.verify_registration_details(registration_code, D.EVENT_DATE, D.STARTING_TIME, D.VENUE)
        return registration_code

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_001", "TC_EV_002"])
    def test_open_explore_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()

    @pytest.mark.skip(reason="needs locators: empty state / no event message on Explore Event")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_003"])
    def test_explore_event_empty_state(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_004", "TC_EV_005"])
    def test_open_event_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_event(event_flow)
        event_flow.see_event_information()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_006"])
    def test_verify_event_package_list(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, event_package_flow: EventPackageFlow):
        D.load(TC_ID)
        PACKAGES = load_package(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_event(event_flow)
        event_package_flow.secure_slot()
        event_package_flow.verify_select_package_screen(PACKAGES)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_007"])
    def test_choose_event_package(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, event_package_flow: EventPackageFlow):
        D.load(TC_ID)
        PACKAGES = load_package(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_event(event_flow)
        event_package_flow.secure_slot()
        event_package_flow.set_packages(PACKAGES)
        event_package_flow.verify_packages_selected(PACKAGES)
        event_package_flow.verify_package_summary(PACKAGES, D.TOTAL_PLAYERS, D.TOTAL_PRICE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_008"])
    def test_cannot_continue_without_event_package(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, event_package_flow: EventPackageFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_event(event_flow)
        event_package_flow.secure_slot()
        event_package_flow.verify_confirm_packages_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_009"])
    def test_event_with_package_opens_registration_confirmation(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, event_package_flow: EventPackageFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        PACKAGES = load_package(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_with_package(event_flow, event_package_flow, PACKAGES)
        event_flow.verify_multi_price_registration(D.EVENT, D.EVENT_DATE, D.STARTING_TIME, D.VENUE, PLAYERS, PACKAGES, D.TOTAL_PRICE, D.REGISTRATION_METHOD)
        event_flow.verify_registration_confirmation_players(PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_010"])
    def test_event_without_package_opens_registration_confirmation(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.verify_registration_confirmation()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_012", "TC_EV_013"])
    def test_verify_event_registration_confirmation_host_only(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.verify_registration_information(D.EVENT_DATE, D.STARTING_TIME, D.VENUE, D.REGISTRATION_METHOD, PLAYERS, D.TOTAL_PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_011"])
    def test_cannot_register_for_closed_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_event(event_flow)
        event_flow.verify_secure_slot_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_014"])
    def test_open_event_add_player_form(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.add_player()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_015"])
    def test_add_event_player_with_valid_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.invite_players(PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_016"])
    def test_cannot_add_event_player_with_empty_fields(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.open_add_player_manually()
        event_flow.verify_save_player_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_017"])
    def test_cannot_add_event_player_with_invalid_format(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.open_add_player_manually()
        event_flow.fill_manual_players(PLAYERS)
        event_flow.verify_save_player_disabled()

    @pytest.mark.skip(reason="needs locators: edit player entry point and edit form on Registration Confirmation")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_018"])
    def test_edit_event_player_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_019"])
    def test_remove_event_player(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.invite_players(PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)
        event_flow.remove_players(PLAYERS)
        event_flow.verify_players_removed(PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_020"])
    def test_promo_auto_applied_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.verify_players_promos(PLAYERS)

    @pytest.mark.skip(reason="needs locators: no promo state on Registration Confirmation promo section")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_021"])
    def test_no_promo_applied_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)

    @pytest.mark.skip(reason="needs locators: remove promo action on Event available promos")
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_022"])
    def test_remove_auto_applied_promo_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_023"])
    def test_choose_event_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        event_flow.verify_registration_confirmation()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_024"])
    def test_cannot_pay_event_without_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.verify_pay_now_disabled()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_025", "TC_EV_026", "TC_EV_027"])
    def test_pay_event_and_see_registration_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        payment_information = self._pay(event_flow)
        self._verify_registration(event_flow, PLAYERS, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_028"])
    def test_event_registration_appears_in_activity(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, cancellation_flow: CancellationFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        self._pay(event_flow)
        event_flow.finish()
        cancellation_flow.open_activity()
        cancellation_flow.find_activity_card(D.EVENT)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TC_EV_029", "TC_EV_030", "TC_EV_031", "TC_EV_032", "TC_EV_033", "TC_EV_034", "TC_EV_035", "TC_EV_036", "TC_EV_037", "TC_EV_038", "TC_EV_039", "TC_EV_040", "TC_EV_041", "TC_EV_042"])
    def test_end_to_end_register_event_host_only(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_registration_without_package(event_flow)
        event_flow.verify_registration_information(D.EVENT_DATE, D.STARTING_TIME, D.VENUE, D.REGISTRATION_METHOD, PLAYERS, D.TOTAL_PLAYERS)
        event_flow.verify_players_promos(PLAYERS)
        payment_information = self._pay(event_flow)
        self._verify_registration(event_flow, PLAYERS, payment_information)
