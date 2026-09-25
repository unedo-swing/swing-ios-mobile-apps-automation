from flows.tee_time_flow import TeeTimeFlow
from pages.tee_time.group_booking_confirmation_page import GroupBookingConfirmationPage
from pages.tee_time.group_booking_intro_page import GroupBookingIntroPage
from pages.tee_time.group_booking_invitation_page import GroupBookingInvitationPage
from pages.tee_time.invite_player_page import InvitePlayerPage
from pages.tee_time.leave_group_booking_page import LeaveGroupBookingPage


class GroupBookingFlow(TeeTimeFlow):
    FLOW_NAME = "GroupBookingFlow"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.intro = self.page(GroupBookingIntroPage)
        self.invite = self.page(InvitePlayerPage)
        self.confirm = self.page(GroupBookingConfirmationPage)
        self.invitation = self.page(GroupBookingInvitationPage)
        self.leave = self.page(LeaveGroupBookingPage)

    def choose_group_booking(self):
        self.method.choose_group_booking()
        self.intro.verify_screen()

    def open_invite_from_intro(self):
        self.intro.tap_invite_friends()
        self.invite.verify_screen()

    def open_invite_more(self):
        self.confirm.tap_invite_more()
        self.invite.verify_screen()

    def pick_friend(self, player):
        self.invite.search_friend(player.get("search_keyword") or player.get("username"))
        self.invite.submit_search()
        self.invite.select_friend(player.get("username") or player.get("player"))
        if self.invite.is_loaded(3) and self.invite.confirm_is_enabled():
            self.invite.tap_confirm()
        assert self.invite.is_closed(), (
            f"Invite a player sheet is still open after picking {player.get('player')}, "
            f"the friend was not selected or the invite was not confirmed")
        self.confirm.verify_screen()

    def invite_group_player(self, player, first=False):
        if first:
            self.open_invite_from_intro()
        else:
            self.open_invite_more()
        self.pick_friend(player)

    def invite_group_players(self, players, total_players=""):
        for index, player in enumerate(self.players_to_invite(players, total_players)):
            self.invite_group_player(player, first=index == 0)
            self.verify_player_added(player["player"])
            self.verify_player_waiting(player["player"])

    def verify_player_waiting(self, player):
        assert self.confirm.is_player_waiting(player, 10), (
            f"{player} is not waiting for confirmation, status {self.confirm.player_status_text(player)!r}")

    def wait_for_player_ready(self, player):
        self.confirm.wait_player_ready(player)

    def wait_for_players_ready(self, players, total_players=""):
        for player in self.players_to_invite(players, total_players):
            self.wait_for_player_ready(player["player"])

    def verify_player_not_joined(self, player):
        self.confirm.wait_player_gone(player)

    def verify_pay_now_enabled(self):
        assert self.confirm.pay_now_is_enabled(), "Pay now is still disabled"

    def verify_pay_now_disabled(self):
        assert not self.confirm.pay_now_is_enabled(), "Pay now is enabled before every player is ready"

    def wait_for_invitation(self):
        self.invitation.verify_screen()

    def verify_invitation(self, host_name, venue):
        text = self.invitation.message_text()
        assert host_name in text and venue in text, (
            f"invitation message does not name {host_name!r} and {venue!r}: {text!r}")

    def accept_invitation(self):
        self.invitation.tap_accept()
        self.confirm.verify_screen()
        self.confirm.verify_editable()

    def decline_invitation(self):
        self.invitation.tap_decline()
        self.home.verify_screen()

    def open_leave_sheet(self):
        self.confirm.tap_back()
        self.leave.verify_screen()

    def leave_group_booking(self):
        self.open_leave_sheet()
        self.leave.tap_leave()
        self.home.verify_screen()

    def stay_in_group_booking(self):
        self.open_leave_sheet()
        self.leave.tap_stay()
        self.confirm.verify_screen()
        self.confirm.verify_editable()

    def set_swing_credits(self, player, on=True):
        self.confirm.set_swing_credits(player, on)

    def mark_ready(self):
        self.confirm.tap_im_ready()
        self.confirm.verify_waiting_for_host()

    def go_back_to_edit(self):
        self.confirm.tap_go_back()
        self.confirm.verify_editable()

    def verify_host_will_pay(self):
        self.confirm.scroll_to_payment_note()
        assert "Host will make the payment" in self.confirm.host_will_pay_text(), (
            "player screen does not say the host will make the payment")

    def prepare_invited_player(self, player):
        if player.get("promo_code"):
            self.redeem_player_promo(player["player"], player["promo_name"], player["promo_code"])
            self.verify_promo_applied(player["player"], player["promo_name"])
        elif player.get("promo_name"):
            self.verify_promo_autoapplied(player["player"], player["promo_name"])
        if player.get("add_ons_name"):
            self.set_player_addons(player["player"], player["add_ons_name"], player.get("add_ons_qty", 1))
