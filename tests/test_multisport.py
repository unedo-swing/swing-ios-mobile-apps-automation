import pytest

from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.multisport_flow import MultisportFlow
from helpers.pdf_report import init_pdf
from test_data.multisport_test_data import MultisportTestData as M


def login(login_flow: LoginFlow, home_flow: HomeFlow):
    login_flow.login_with_otp(M.COUNTRY_NAME, M.PHONE_NUMBER, M.METHOD_VERIFICATION, M.OTP)
    home_flow.skip_first_run_screens(M.SPORT_TYPE)
    home_flow.verify_home()


class TestMultisportFlow:

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_001"])
    def test_multisport_select_sport(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_002"])
    def test_multisport_select_venue(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_003"])
    def test_multisport_book_venue(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_004"])
    def test_multisport_select_schedule(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_005"])
    def test_multisport_add_player(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_006"])
    def test_multisport_remove_player(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)
        multisport_flow.remove_player()

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_007"])
    def test_multisport_select_payment(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)
        multisport_flow.payment_method_flow(M.PAYMENT_METHOD)

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_009"])
    def test_multisport_add_additional(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_additional_items_flow(M.items_list())
        multisport_flow.confirm_additional_item()

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_010"])
    def test_multisport_add_additional_multiple(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_additional_items_flow(M.items_list())
        multisport_flow.confirm_additional_item()

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_011"])
    def test_multisport_remove_additional(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_additional_items_flow(M.items_list())
        multisport_flow.remove_additional_item(M.items_list())

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_012"])
    def test_multisport_remove_additional_multiple(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_additional_items_flow(M.items_list())
        multisport_flow.remove_additional_item(M.items_list())

    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_013"])
    def test_multisport_can_select_one_schedule(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()



class TestMultisportFlowPayment:

    @pytest.mark.skip(reason="skipped on Android too: real payment")
    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_008"])
    def test_multisport_end_to_end_payment(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)
        multisport_flow.payment_method_flow(M.PAYMENT_METHOD)
        multisport_flow.pay_now()
        multisport_flow.finish()

    @pytest.mark.skip(reason="skipped on Android too: real payment")
    @pytest.mark.app_reset("clear")
    @pytest.mark.multisport
    @pytest.mark.parametrize("TC_ID", ["TC_MLTS_014"])
    def test_multisport_end_to_end_payment_with_add_on(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, multisport_flow: MultisportFlow):
        M.load(TC_ID)
        pdf = init_pdf(M.TC_NAME, tc_id=TC_ID)
        login(login_flow, home_flow)

        multisport_flow.open_multisport_sport()
        multisport_flow.select_sport(M.SPORT_NAME)
        multisport_flow.view_all_venue()
        multisport_flow.select_venue(M.VENUE_NAME)
        multisport_flow.book_venue()
        multisport_flow.select_schedule_flow(M.TITLE_SCHEDULE, M.HOW_MUCH_SCHEDULE)
        multisport_flow.confirm_schedule()
        multisport_flow.add_additional_items_flow(M.items_list())
        multisport_flow.confirm_additional_item()
        multisport_flow.add_player_by_name(M.PLAYER_NAME)
        multisport_flow.payment_method_flow(M.PAYMENT_METHOD)
        multisport_flow.pay_now()
        multisport_flow.finish()

