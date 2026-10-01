import pytest

from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.tee_time_flow import TeeTimeFlow
from helpers.pdf_report import init_pdf
from test_data.add_ons_data import load_add_ons
from test_data.player_data import load_players
from test_data.tee_time_test_data import TeeTimeTestData as D


class TestTeeTime:

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

    def _open_standard_booking(self, tee_time_flow: TeeTimeFlow):
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)
        tee_time_flow.choose_date(D.BOOKING_DATE)
        tee_time_flow.choose_session(D.SESSION)
        tee_time_flow.choose_tee_time(D.PREFERRED_TIME)
        tee_time_flow.book_tee_time()
        tee_time_flow.choose_standard_booking()
    
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_001", "TT_002", "TT_003"])
    def test_verify_page_explore_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_004"])
    def test_verify_page_explore_tee_time_swing_pass_only(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time(D.MEMBER_TYPE)
        tee_time_flow.only_swing_pass_partners(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_005"])
    def test_verify_search_result_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.skip
    @pytest.mark.parametrize("TC_ID", ["TT_006"])
    def test_verify_page_tee_time_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)
        tee_time_flow.see_all_details_sections()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_007", "TT_008", "TT_009"])
    def test_verify_featured_promo_swing_pass_tee_time_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)
        tee_time_flow.verify_button_exclusive_featured_promo(D.MEMBER_TYPE)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_010"])
    def test_verify_see_all_featured_promo_tee_time_details(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)
        tee_time_flow.open_featured_promos()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_011"])
    def test_verify_booking_method_tee_time(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        tee_time_flow.open_tee_time()
        tee_time_flow.open_search()
        tee_time_flow.search_golf_course(D.SEARCH_KEYWORD)
        tee_time_flow.open_result(D.VENUE)
        tee_time_flow.choose_date(D.BOOKING_DATE)
        tee_time_flow.choose_session(D.SESSION)
        tee_time_flow.choose_tee_time(D.PREFERRED_TIME)
        tee_time_flow.book_tee_time()

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_012"])
    def test_verify_booking_confirmation_standard_booking(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_013", "TT_014", "TT_015"])
    def test_verify_auto_applied_promo_host_only(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_016"])
    def test_booking_standard_host_only_with_auto_applied_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_players_used_credits(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_017"])
    def test_booking_standard_invite_player_with_auto_applied_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)
        tee_time_flow.invite_players_only_with_autoapplied_promo(PLAYERS, D.TOTAL_PLAYERS)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_players_used_credits(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)

        
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_018"])
    def test_booking_standard_host_only_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.use_swing_credits(D.HOST_NAME)
        tee_time_flow.verify_players_promos(PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_players_used_credits(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)
        
        
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_019"])
    def test_booking_standard_invite_player_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.use_swing_credits(D.HOST_NAME)
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.invite_players_and_remove_promos(PLAYERS, total_players=D.TOTAL_PLAYERS)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_payment_information(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_payment_information(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_020"])
    def test_booking_standard_host_only_with_apply_and_redeem_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.redeem_player_promo(D.HOST_NAME, D.PROMO_NAME, D.PROMO_CODE)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_payment_information(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_payment_information(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_021"])
    def test_booking_standard_invite_player_with_apply_and_redeem_promo_each_player(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.redeem_player_promo(D.HOST_NAME, D.PROMO_NAME, D.PROMO_CODE)
        tee_time_flow.invite_players_and_redeemed_promos(PLAYERS, total_players=D.TOTAL_PLAYERS)
        tee_time_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_payment_information(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_payment_information(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information)
                
        
    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.parametrize("TC_ID", ["TT_022"])
    def test_booking_standard_host_only_used_credit_without_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.use_swing_credits(D.HOST_NAME)
        tee_time_flow.verify_players_promos(PLAYERS)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.verify_players_used_credits(payment_information, PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)
        tee_time_flow.back_to_activity()
        tee_time_flow.open_home_tab()
        tee_time_flow.open_swing_credits()
        tee_time_flow.open_swing_credit_history()
        tee_time_flow.verify_used_credit_booking_code_players(booking_code, payment_information, PLAYERS, D.HOST_NAME)

    def _verify_regression_booking(self, tee_time_flow: TeeTimeFlow, PLAYERS, payment_information, payment_method=""):
        tee_time_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        booking_code = tee_time_flow.get_booking_code_after_payment()
        tee_time_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, payment_method)
        tee_time_flow.open_booking_details()
        tee_time_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["TT_REGRESS_GSA_001"])
    def test_regression_existing_book_tee_time_with_credit_card(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.link_new_credit_card(D.HOST_NAME, D.CARD_NUMBER, D.CARD_EXPIRY, D.CARD_CVV, D.CARD_OTP)
        payment_information = tee_time_flow.get_payment_information_before_payment("0", PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now_with_credit_card(D.CARD_CVV, D.CARD_OTP)
        self._verify_regression_booking(tee_time_flow, PLAYERS, payment_information)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression_existing
    @pytest.mark.parametrize("TC_ID", ["TT_REGRESS_GSA_002", "TT_REGRESS_GSA_003", "TT_REGRESS_GSA_004", "TT_REGRESS_GSA_005", "TT_REGRESS_GSA_006", "TT_REGRESS_GSA_007", "TT_REGRESS_GSA_008", "TT_REGRESS_GSA_009", "TT_REGRESS_GSA_010", "TT_REGRESS_GSA_011", "TT_REGRESS_GSA_012", "TT_REGRESS_GSA_013", "TT_REGRESS_GSA_014"])
    def test_regression_existing_book_tee_time_by_payment_method(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, tee_time_flow: TeeTimeFlow):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        self._login(login_flow, home_flow)
        self._open_standard_booking(tee_time_flow)
        tee_time_flow.remove_promo(D.HOST_NAME)
        tee_time_flow.choose_payment_method(D.PAYMENT_METHOD)
        payment_information = tee_time_flow.get_payment_information_before_payment("0", PLAYERS, D.HOST_NAME)
        tee_time_flow.pay_now()
        self._verify_regression_booking(tee_time_flow, PLAYERS, payment_information, D.PAYMENT_METHOD)
