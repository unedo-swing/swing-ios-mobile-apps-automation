from locators.event.registration_details_locators import RegistrationDetailsLocators as L
from pages.base_page import BasePage


class RegistrationDetailsPage(BasePage):
    ROOT_LOCATOR = L.EL_HEADER
    PAGE_NAME = "RegistrationDetailsPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_HEADER, timeout=20), "Registration details screen not shown"
        # assert self.is_visible(L.TXT_QR_TITLE, timeout=5), "Registration details QR code not shown"
        assert self.is_visible(L.TXT_REGISTRATION_CODE, timeout=5), "Registration details code not shown"
        assert self.is_visible(L.BTN_SEE_BREAKDOWN, timeout=5), "Registration details breakdown button not shown"
        self.capture_step("registration_details")
        return self

    def open_breakdown(self):
        self.capture_step("open_breakdown")
        self.click(L.BTN_SEE_BREAKDOWN)

    def open_leaderboard(self):
        self.capture_step("open_leaderboard")
        self.click(L.EL_LEADERBOARD_BANNER)

    def open_more(self):
        self.capture_step("open_more")
        self.click(L.BTN_MORE)

    def scroll_to_flight_arrangement(self):
        self.capture_step("scroll_to_flight_arrangement")
        self.scroll_to(L.TXT_FLIGHT_TITLE)

    def tap_back(self):
        self.capture_step("tap_back")
        self.click(L.BTN_BACK)

    def qr_code_text(self):
        return self.label_of(L.TXT_QR_CODE)

    def qr_note_text(self):
        return self.label_of(L.TXT_QR_NOTE)

    def status_text(self):
        return self.label_of(L.TXT_STATUS)

    def registration_code_text(self):
        return self.label_of(L.TXT_REGISTRATION_CODE)

    def value_of_label(self, label):
        return self.label_of(L.TXT_VALUE_BY_LABEL.format(label))

    def date_text(self):
        return self.label_of(L.TXT_VALUE_BY_LABEL.format("Date"))

    def starting_time_text(self):
        return self.label_of(L.TXT_VALUE_BY_LABEL.format("Starting time"))

    def venue_text(self):
        return self.label_of(L.TXT_VALUE_BY_LABEL.format("Venue"))

    def unassigned_slot_count(self):
        return self.count(L.LIST_UNASSIGNED_SLOTS)

    def has_status(self, name, timeout=5):
        return self.is_visible(L.TXT_STATUS_BY_NAME.format(name), timeout)

    def has_flight(self, name, timeout=5):
        return self.is_visible(L.EL_FLIGHT_BY_NAME.format(name), timeout)
