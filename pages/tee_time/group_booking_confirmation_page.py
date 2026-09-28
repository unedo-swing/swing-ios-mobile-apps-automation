from locators.tee_time.group_booking_confirmation_locators import GroupBookingConfirmationLocators as G
from locators.tee_time.booking_confirmation_locators import TeeTimeBookingConfirmationLocators as L
from selenium.common.exceptions import TimeoutException

from helpers import waits
from pages.tee_time.booking_confirmation_page import TeeTimeBookingConfirmationPage


class GroupBookingConfirmationPage(TeeTimeBookingConfirmationPage):
    ROOT_LOCATOR = G.EL_HEADER
    PAGE_NAME = "GroupBookingConfirmationPage"
    READY_TIMEOUT = 180

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(G.EL_HEADER, timeout=20), "Group booking confirmation screen not shown"
        assert self.is_visible(G.TXT_COUNTDOWN, timeout=10), "Group booking countdown not shown"
        self.capture_step("group_booking_confirmation")
        return self

    def verify_editable(self):
        assert self.is_visible(L.BTN_BACK, timeout=10), "Group booking back button not shown"
        assert self.is_visible(G.BTN_IM_READY, timeout=5), "I'm ready button not shown"
        self.capture_step("group_booking_editable")
        return self

    def verify_waiting_for_host(self):
        assert self.is_visible(G.EL_WAITING_HOST, timeout=20), "Waiting for host and others not shown"
        assert self.is_visible(G.BTN_GO_BACK, timeout=5), "Go back button not shown"
        self.capture_step("group_booking_waiting_for_host")
        return self

    def go_to_top(self):
        self.scroll_to(G.TXT_BOOKING_TYPE, "down", 3)

    def booking_type_text(self):
        return self.label_of(G.TXT_BOOKING_TYPE)

    def tap_invite_more(self):
        self.capture_step("tap_invite_more")
        self.scroll_and_click(G.BTN_INVITE_MORE)

    def tap_im_ready(self):
        self.capture_step("tap_im_ready")
        self.click(G.BTN_IM_READY)

    def tap_go_back(self):
        self.capture_step("tap_go_back")
        self.click(G.BTN_GO_BACK)

    def set_swing_credits(self, player, on=True):
        self.set_switch(G.SWITCH_USE_CREDITS_PLAYER.format(player), on)
        self.capture_step("set_swing_credits", f"{player} = {on}")

    def swing_credits_is_on(self, player):
        return self.is_selected(G.SWITCH_USE_CREDITS_PLAYER.format(player))

    def player_status_text(self, player):
        return self.label_of(G.EL_PLAYER_STATUS.format(player))

    def is_player_ready(self, player, timeout=3):
        return self.is_present(G.EL_PLAYER_READY.format(player), timeout)

    def is_player_waiting(self, player, timeout=3):
        return self.is_present(G.EL_PLAYER_WAITING.format(player), timeout)

    def wait_player_ready(self, player, timeout=None):
        self.bring_into_view(L.IMG_PLAYER_BY_NAME.format(player), "down")
        try:
            waits.wait_until_true(lambda: self.is_player_ready(player, 2), timeout or self.READY_TIMEOUT,
                                  interval=2, message=f"{player} is not ready")
        except TimeoutException:
            self.capture_step("player_not_ready", player)
            return False
        self.capture_step("player_ready", player)
        return True

    def wait_player_gone(self, player, timeout=None):
        waits.wait_until_true(lambda: not self.has_player(player, 2), timeout or self.READY_TIMEOUT,
                              interval=2, message=f"{player} is still in the group booking")
        self.capture_step("player_gone", player)
        return self

    def has_invite_more(self, timeout=5):
        return self.is_visible(G.BTN_INVITE_MORE, timeout)

    def scroll_to_payment_note(self):
        self.scroll_to(G.TXT_HOST_WILL_PAY)

    def host_will_pay_text(self):
        return self.label_of(G.TXT_HOST_WILL_PAY)

    def has_cancel_group_booking(self, timeout=5):
        return self.is_visible(G.TXT_CANCEL_GROUP_BOOKING, timeout)

    def pay_now_is_enabled(self):
        return self.is_enabled(G.BTN_PAY_NOW)
