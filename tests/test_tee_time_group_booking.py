import pytest

from fixtures.player_fixtures import PlayerDevices
from flows.group_booking_flow import GroupBookingFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from helpers.pdf_report import init_pdf
from test_data.player_data import load_players
from test_data.tee_time_test_data import TeeTimeTestData as D


class TestTeeTimeGroupBooking:

    def _login(self, login_flow: LoginFlow, home_flow: HomeFlow, country, phone_number, method, otp):
        login_flow.open_login()
        login_flow.choose_country(country)
        login_flow.enter_phone_number(phone_number)
        login_flow.continue_log_in()
        login_flow.choose_verification_method(method)
        login_flow.verify_page_code_otp()
        login_flow.enter_otp_code(otp, country, phone_number)
        home_flow.select_sport_if_shown(D.SPORT_TYPE)
        home_flow.enable_notifications_if_shown()
        home_flow.enable_location_if_shown()
        home_flow.dismiss_coachmark_if_shown()
        home_flow.close_whats_new_if_shown()
        home_flow.verify_home()

    def _open_players(self, PLAYERS, player_devices: PlayerDevices, host_group_flow: GroupBookingFlow):
        devices = player_devices.open_all(host_group_flow.players_to_invite(PLAYERS, D.TOTAL_PLAYERS))
        for device in devices:
            self._login(device.login, device.home,
                        device.player["country_name"] or D.PLAYER_COUNTRY_NAME,
                        device.player["phone_number"],
                        device.player["verification_method"] or D.PLAYER_METHOD_VERIFICATION,
                        D.PLAYER_OTP)
        return devices

    def _login_host(self, login_flow: LoginFlow, home_flow: HomeFlow):
        self._login(login_flow, home_flow, D.COUNTRY_NAME, D.PHONE_NUMBER, D.METHOD_VERIFICATION, D.OTP)

    def _open_group_booking(self, host_group_flow: GroupBookingFlow):
        host_group_flow.open_tee_time()
        host_group_flow.open_search()
        host_group_flow.search_golf_course(D.SEARCH_KEYWORD)
        host_group_flow.open_result(D.VENUE)
        host_group_flow.choose_date(D.BOOKING_DATE)
        host_group_flow.choose_session(D.SESSION)
        host_group_flow.choose_tee_time(D.PREFERRED_TIME)
        host_group_flow.book_tee_time()
        host_group_flow.choose_group_booking()

    def _invite(self, PLAYERS, host_group_flow: GroupBookingFlow):
        host_group_flow.invite_group_players(PLAYERS, D.TOTAL_PLAYERS)
        host_group_flow.verify_auto_applied_promos_host(D.HOST_NAME, D.PROMO_NAME)

    def _receive_invitation(self, device):
        device.group.wait_for_invitation()
        device.group.verify_invitation(D.HOST_NAME, D.VENUE)

    def _accept_all(self, devices):
        for device in devices:
            self._receive_invitation(device)
            device.group.accept_invitation()

    def _ready_all(self, devices, use_credits=False):
        for device in devices:
            device.group.prepare_invited_player(device.player)
            if use_credits:
                device.group.set_swing_credits(device.name, True)
            device.group.mark_ready()
            device.group.verify_host_will_pay()

    def _host_pays_and_verifies(self, PLAYERS, host_group_flow: GroupBookingFlow):
        host_group_flow.wait_for_players_ready(PLAYERS, D.TOTAL_PLAYERS)
        host_group_flow.verify_booking_confirmation(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, D.BOOKING_METHOD, D.TOTAL_PLAYERS)
        host_group_flow.choose_payment_method(D.PAYMENT_METHOD)
        host_group_flow.verify_pay_now_enabled()
        payment_information = host_group_flow.get_payment_information_before_payment("1", PLAYERS, D.HOST_NAME)
        host_group_flow.verify_payment_information(payment_information, PLAYERS, D.HOST_NAME)
        host_group_flow.verify_players_used_credits(payment_information, PLAYERS, D.HOST_NAME)
        host_group_flow.pay_now()
        booking_code = host_group_flow.get_booking_code_after_payment()
        host_group_flow.verify_payment_success_players(D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS, D.VENUE, D.PAYMENT_METHOD)
        host_group_flow.open_booking_details()
        host_group_flow.verify_booking_details_players(booking_code, D.BOOKING_DATE, D.SESSION, D.PREFERRED_TIME, payment_information, PLAYERS)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.timeout(1800)
    @pytest.mark.parametrize("TC_ID", ["TT_GB_001"])
    def test_group_booking_player_accepts_with_auto_applied_promo(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, host_group_flow: GroupBookingFlow, player_devices: PlayerDevices):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        devices = self._open_players(PLAYERS, player_devices, host_group_flow)
        self._login_host(login_flow, home_flow)
        self._open_group_booking(host_group_flow)
        self._invite(PLAYERS, host_group_flow)
        self._accept_all(devices)
        self._ready_all(devices)
        self._host_pays_and_verifies(PLAYERS, host_group_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.timeout(1800)
    @pytest.mark.parametrize("TC_ID", ["TT_GB_002"])
    def test_group_booking_player_redeems_promo_uses_credits_and_add_ons(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, host_group_flow: GroupBookingFlow, player_devices: PlayerDevices):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        devices = self._open_players(PLAYERS, player_devices, host_group_flow)
        self._login_host(login_flow, home_flow)
        self._open_group_booking(host_group_flow)
        self._invite(PLAYERS, host_group_flow)
        self._accept_all(devices)
        self._ready_all(devices, use_credits=True)
        self._host_pays_and_verifies(PLAYERS, host_group_flow)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.timeout(1800)
    @pytest.mark.parametrize("TC_ID", ["TT_GB_003"])
    def test_group_booking_player_declines_invitation(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, host_group_flow: GroupBookingFlow, player_devices: PlayerDevices):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        devices = self._open_players(PLAYERS, player_devices, host_group_flow)
        self._login_host(login_flow, home_flow)
        self._open_group_booking(host_group_flow)
        host_group_flow.invite_group_players(PLAYERS, D.TOTAL_PLAYERS)
        for device in devices:
            self._receive_invitation(device)
            device.group.decline_invitation()
            host_group_flow.verify_player_not_joined(device.name)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.timeout(1800)
    @pytest.mark.parametrize("TC_ID", ["TT_GB_004"])
    def test_group_booking_player_leaves_group_booking(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, host_group_flow: GroupBookingFlow, player_devices: PlayerDevices):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        devices = self._open_players(PLAYERS, player_devices, host_group_flow)
        self._login_host(login_flow, home_flow)
        self._open_group_booking(host_group_flow)
        self._invite(PLAYERS, host_group_flow)
        self._accept_all(devices)
        for device in devices:
            device.group.leave_group_booking()
            host_group_flow.verify_player_not_joined(device.name)

    @pytest.mark.app_reset("clear")
    @pytest.mark.regression
    @pytest.mark.timeout(1800)
    @pytest.mark.parametrize("TC_ID", ["TT_GB_005"])
    def test_group_booking_player_stays_goes_back_and_host_pays(self, TC_ID, login_flow: LoginFlow, home_flow: HomeFlow, host_group_flow: GroupBookingFlow, player_devices: PlayerDevices):
        D.load(TC_ID)
        PLAYERS = load_players(TC_ID)
        pdf = init_pdf(D.TC_NAME, tc_id=TC_ID)
        devices = self._open_players(PLAYERS, player_devices, host_group_flow)
        self._login_host(login_flow, home_flow)
        self._open_group_booking(host_group_flow)
        self._invite(PLAYERS, host_group_flow)
        self._accept_all(devices)
        for device in devices:
            device.group.stay_in_group_booking()
            device.group.mark_ready()
            device.group.go_back_to_edit()
            device.group.remove_promo_and_verify(device.name)
            device.group.mark_ready()
        self._host_pays_and_verifies(PLAYERS, host_group_flow)
