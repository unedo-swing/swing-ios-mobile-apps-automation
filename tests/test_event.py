import pytest

from flows.event_flow import EventFlow
from flows.event_package_flow import EventPackageFlow
from flows.player_details_flow import PlayerDetailsFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.payment_callback_flow import PaymentCallbackFlow
from helpers.pdf_report import init_pdf
from test_data.event_test_data import EventTestData as D
from test_data.player_data import load_players
from test_data.event_package import load_package
from test_data.player_details_data import load_player_details


class TestEvent:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow):
        login_flow.open_login()
        login_flow.choose_country(D.COUNTRY_NAME)
        login_flow.enter_phone_number(D.PHONE_NUMBER)
        login_flow.continue_log_in()
        login_flow.choose_verification_method(D.METHOD_VERIFICATION)
        login_flow.verify_page_code_otp()
        login_flow.enter_otp_code(D.OTP, D.COUNTRY_NAME, D.PHONE_NUMBER)
        home_flow.select_sport_if_shown(D.SPORT_TYPE)
        home_flow.enable_notifications_if_shown()
        home_flow.enable_location_if_shown()
        home_flow.dismiss_coachmark_if_shown()
        home_flow.close_whats_new_if_shown()
        home_flow.verify_home()

    def _open_standard_registration_single_price(self, event_flow: EventFlow):
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)
        event_flow.secure_slot()
        event_flow.choose_standard_registration()
    
    def _open_standard_registration_multi_price(self, event_flow: EventFlow):
        PACKAGES = load_package(D.TC_ID) 
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)
        event_flow.secure_slot()
        event_flow.select_package(PACKAGES)
        event_flow.choose_standard_registration()

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_001", "EVENT_002", "EVENT_003"])
    def test_verify_page_explore_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_004"])
    def test_verify_page_explore_event_swing_pass_only(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()
        event_flow.only_swing_pass_partners()

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_005"])
    def test_verify_page_event_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)
        event_flow.see_event_information()

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_006"])
    def test_verify_registration_method_event(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)
        event_flow.secure_slot()

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_007"])
    def test_verify_registration_confirmation_standard_single_price(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_registration_single_price(event_flow)
        event_flow.verify_registration_information(D.EVENT_DATE, D.STARTING_TIME, D.VENUE, D.REGISTRATION_METHOD, PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)


    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_011", "EVENT_012"])
    def test_registration_event_host_only_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        # self._login(login_flow, home_flow)
        self._open_standard_registration_single_price(event_flow)
        event_flow.fill_host_details(PLAYERS, D.QUESTION_ANSWER)
        event_flow.verify_registration_information(D.EVENT_DATE, D.STARTING_TIME, D.VENUE, D.REGISTRATION_METHOD, PLAYERS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        registration_code = event_flow.get_registration_code_after_payment()
        event_flow.verify_payment_success_event(D.EVENT_DATE, D.STARTING_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        event_flow.open_registration_details()
        event_flow.verify_registration_details(registration_code, D.EVENT_DATE, D.STARTING_TIME, D.VENUE)

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_013", "EVENT_014", "EVENT_015", "EVENT_016"])
    def test_registration_event_with_invited_players(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_registration_single_price(event_flow)
        event_flow.fill_host_details(PLAYERS, D.QUESTION_ANSWER)
        event_flow.invite_players_with_details(PLAYERS, D.QUESTION_ANSWER)
        event_flow.apply_player_promos(PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)
        event_flow.verify_players_promos(PLAYERS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        registration_code = event_flow.get_registration_code_after_payment()
        event_flow.verify_payment_success_event(D.EVENT_DATE, D.STARTING_TIME, payment_information,
                                                PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        event_flow.open_registration_details()
        event_flow.verify_registration_details(registration_code, D.EVENT_DATE, D.STARTING_TIME, D.VENUE)

    @pytest.mark.app_reset("force-close")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["EVENT_017"])
    def test_registration_event_multi_package_with_player_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, event_package_flow: EventPackageFlow, player_details_flow: PlayerDetailsFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        PACKAGES = load_package(TC_ID)
        DETAILS = load_player_details(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        event_flow.open_events()
        event_flow.find_event(D.EVENT)
        event_flow.open_event(D.EVENT)
        event_package_flow.secure_slot()
        event_package_flow.verify_select_package_screen(PACKAGES)
        event_package_flow.set_packages(PACKAGES)
        event_package_flow.verify_packages_selected(PACKAGES)
        event_package_flow.verify_package_summary(PACKAGES, D.TOTAL_PLAYERS, D.TOTAL_PRICE)
        event_package_flow.confirm_packages()
        event_flow.choose_standard_registration()
        event_flow.verify_multi_price_registration(D.EVENT, D.EVENT_DATE, D.STARTING_TIME, D.VENUE,
                                                   PLAYERS, PACKAGES, D.TOTAL_PRICE, D.REGISTRATION_METHOD)
        event_flow.invite_players(PLAYERS)
        event_flow.verify_registration_confirmation_players(PLAYERS)
        player_details_flow.fill_players_details(PLAYERS, DETAILS)
        player_details_flow.verify_players_details(PLAYERS, DETAILS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        registration_code = event_flow.get_registration_code_after_payment()
        event_flow.verify_payment_success_event(D.EVENT_DATE, D.STARTING_TIME, payment_information,
                                                PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        event_flow.open_registration_details()
        event_flow.verify_registration_details(registration_code, D.EVENT_DATE, D.STARTING_TIME, D.VENUE)


    def _open_regression_registration(self, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, PLAYERS):
        self._login(login_flow, home_flow)
        self._open_standard_registration_single_price(event_flow)
        event_flow.invite_players_with_details(PLAYERS, D.QUESTION_ANSWER)
        event_flow.verify_registration_information(D.EVENT_DATE, D.STARTING_TIME, D.VENUE, D.REGISTRATION_METHOD, PLAYERS, D.TOTAL_PLAYERS)

    def _verify_regression_registration(self, event_flow: EventFlow, payment_callback_flow: PaymentCallbackFlow, PLAYERS, payment_information, payment_method=""):
        registration_code = event_flow.get_registration_code_after_payment()
        event_flow.verify_payment_success_event(D.EVENT_DATE, D.STARTING_TIME, payment_information, PLAYERS, D.VENUE, payment_method, D.TOTAL_PLAYERS)
        event_flow.open_registration_details()
        event_flow.verify_registration_details(registration_code, D.EVENT_DATE, D.STARTING_TIME, D.VENUE)
        payment_callback_flow.verify_existing_payment_callback(registration_code)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["EVENT_REGRESS_GSA_001"])
    def test_regression_existing_register_event_with_credit_card(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, payment_callback_flow: PaymentCallbackFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_regression_registration(login_flow, home_flow, event_flow, PLAYERS)
        event_flow.link_new_credit_card(D.CARD_NAME, D.CARD_NUMBER, D.CARD_EXPIRY, D.CARD_CVV, D.CARD_OTP)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now_with_credit_card(D.CARD_CVV, D.CARD_OTP)
        self._verify_regression_registration(event_flow, payment_callback_flow, PLAYERS, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["EVENT_REGRESS_GSA_003", "EVENT_REGRESS_GSA_004", "EVENT_REGRESS_GSA_005", "EVENT_REGRESS_GSA_006"])
    def test_regression_existing_register_event_with_ewallet(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, payment_callback_flow: PaymentCallbackFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_regression_registration(login_flow, home_flow, event_flow, PLAYERS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        self._verify_regression_registration(event_flow, payment_callback_flow, PLAYERS, payment_information, D.PAYMENT_METHOD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["EVENT_REGRESS_GSA_002"])
    def test_regression_existing_register_event_with_qris(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, payment_callback_flow: PaymentCallbackFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_regression_registration(login_flow, home_flow, event_flow, PLAYERS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        event_flow.simulate_gateway_payment(D.PAYMENT_METHOD, "QRIS")
        self._verify_regression_registration(event_flow, payment_callback_flow, PLAYERS, payment_information, D.PAYMENT_METHOD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["EVENT_REGRESS_GSA_007", "EVENT_REGRESS_GSA_008", "EVENT_REGRESS_GSA_009", "EVENT_REGRESS_GSA_010", "EVENT_REGRESS_GSA_011", "EVENT_REGRESS_GSA_012", "EVENT_REGRESS_GSA_013", "EVENT_REGRESS_GSA_014"])
    def test_regression_existing_register_event_with_virtual_account(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, event_flow: EventFlow, payment_callback_flow: PaymentCallbackFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._open_regression_registration(login_flow, home_flow, event_flow, PLAYERS)
        event_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = event_flow.get_payment_information_before_payment("0")
        event_flow.pay_now()
        event_flow.simulate_gateway_payment(D.PAYMENT_METHOD, "Virtual account")
        self._verify_regression_registration(event_flow, payment_callback_flow, PLAYERS, payment_information, D.PAYMENT_METHOD)
