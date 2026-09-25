from locators.tee_time.group_booking_intro_locators import GroupBookingIntroLocators as L
from pages.base_page import BasePage


class GroupBookingIntroPage(BasePage):
    ROOT_LOCATOR = L.TXT_TITLE
    PAGE_NAME = "GroupBookingIntroPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.TXT_TITLE, timeout=20), "Group booking intro sheet not shown"
        assert self.is_visible(L.TXT_SUBTITLE, timeout=5), "Group booking intro subtitle not shown"
        assert self.is_visible(L.TXT_CASHBACK, timeout=5), "Group booking cashback note not shown"
        assert self.is_visible(L.BTN_INVITE_FRIENDS, timeout=5), "Invite friends button not shown"
        self.capture_step("group_booking_intro")
        return self

    def tap_invite_friends(self):
        self.capture_step("tap_invite_friends")
        self.click(L.BTN_INVITE_FRIENDS)

    def title_text(self):
        return self.label_of(L.TXT_TITLE)

    def invite_step_text(self):
        return self.label_of(L.IMG_STEP_INVITE)

    def promos_step_text(self):
        return self.label_of(L.IMG_STEP_PROMOS)

    def host_pays_step_text(self):
        return self.label_of(L.IMG_STEP_HOST_PAYS)

    def cashback_text(self):
        return self.label_of(L.TXT_CASHBACK)

    def has_sheet(self, timeout=3):
        return self.is_visible(L.TXT_TITLE, timeout)
