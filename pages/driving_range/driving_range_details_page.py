from locators.driving_range.driving_range_details_locators import DrivingRangeDetailsLocators as L
from pages.base_page import BasePage


class DrivingRangeDetailsPage(BasePage):
    ROOT_LOCATOR = L.EL_HEADER
    PAGE_NAME = "DrivingRangeDetailsPage"

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.EL_HEADER, timeout=20), "Driving range details screen not shown"
        # assert self.is_visible(L.TXT_SELECT_TIME_TITLE, timeout=5), "Driving range time selector not shown"
        assert self.is_visible(L.BTN_BOOK, timeout=5), "Driving range book button not shown"
        self.capture_step("Verify driving range details page")
        return self

    def verify_all_sections(self):
        self.verify_screen()
        assert self.is_visible(L.IMG_HERO, timeout=10), "Driving range hero image not shown"
        assert self.is_visible(L.TXT_LOCATION, timeout=5), "Driving range city not shown"
        assert self.is_visible(L.TXT_DISTANCE, timeout=5), "Driving range distance not shown"
        assert self.visible_count(L.LIST_PROMOS) > 0, "Driving range promo section not shown"
        assert self.is_visible(L.EL_CASHBACK_BANNER, timeout=5), "Driving range cashback banner not shown"
        assert self.is_visible(L.BTN_CALENDAR, timeout=5), "Driving range calendar button not shown"
        assert self.visible_count(L.LIST_DATE_STRIP) > 0, "Driving range date strip not shown"
        self.capture_step("Verify driving range details overview")
        self.scroll_to(L.TXT_DURATION_TITLE)
        assert self.visible_count(L.LIST_TIME_SLOTS) > 0, "Driving range time slots not shown"
        assert self.visible_count(L.LIST_DURATIONS) > 0, "Driving range duration options not shown"
        self.capture_step("Verify driving range details schedule")
        self.scroll_to(L.BTN_GOOGLE_MAPS)
        assert self.is_visible(L.TXT_LOCATION_TITLE, timeout=5), "Driving range location section not shown"
        assert self.is_visible(L.TXT_ADDRESS, timeout=5), "Driving range address not shown"
        assert self.is_visible(L.TXT_DISTANCE_FROM_LOCATION, timeout=5), "Driving range distance from location not shown"
        assert self.is_visible(L.EL_MAP, timeout=5), "Driving range map not shown"
        assert self.is_visible(L.BTN_GOOGLE_MAPS, timeout=5), "Driving range Google Maps button not shown"
        self.capture_step("Verify driving range details location")
        self.scroll_to(L.TXT_MORE_INFORMATION)
        assert self.is_visible(L.TXT_DESCRIPTION, timeout=5), "Driving range description not shown"
        assert self.is_visible(L.BTN_BOOK, timeout=5), "Driving range book button not shown"
        self.capture_step("Verify driving range details more information")
        return self

    def select_date(self, label):
        self.capture_step("select_date")
        self.click(L.TXT_DATE_BY_LABEL.format(label))

    def open_date_picker(self):
        self.capture_step("Open date picker")
        self.click(L.BTN_CALENDAR)

    def select_bay_type(self, name: str = ""):
        self.capture_step("Select bay type", name)
        self.click(L.EL_TAB_BAY_TYPE.format(name))

    def select_time(self, time_start, time_end=None):
        self.capture_step("Select time", f"{time_start}, {time_end}")
        value_times = self.time_slots(time_start, time_end)
        for value in value_times:
            self.scroll_to(L.TXT_TIME_SLOT.format(value))
            self.click(L.TXT_TIME_SLOT.format(value))

    def select_duration(self, duration):
        self.capture_step("select_duration")
        self.scroll_and_click(L.TXT_DURATION_OPTION.format(duration))

    def open_featured_promos(self):
        self.capture_step("open_featured_promos")
        self.swipe_left_to_element(L.BTN_SEE_ALL_PROMOS, L.EL_PROMO_STRIP)
        self.click(L.BTN_SEE_ALL_PROMOS)
    
    def verify_exclusive_swing_pass_promo(self, player_type: str):
        match player_type:
            case "swing-pass":
                assert self.is_visible(L.BTN_PROMO_ACTIVE), "Not Found"
            case "regular-player":
                assert self.is_visible(L.BTN_PROMO_JOIN), "Not Found"
            case "expired-player":
                assert self.is_visible(L.BTN_PROMO_RENEW), "Not Found"
            case _:
                print("Nothing Comes")
        
        return self
        

    def swipe_to_promo(self, name):
        self.capture_step("swipe_to_promo")
        self.swipe_left_to_element(L.IMG_PROMO_BY_NAME.format(name), L.EL_PROMO_STRIP)

    def swipe_to_date(self, label):
        self.capture_step("swipe_to_date")
        self.swipe_left_to_element(L.TXT_DATE_BY_LABEL.format(label), L.EL_DATE_STRIP)

    def swipe_to_duration(self, duration):
        self.capture_step("swipe_to_duration")
        self.swipe_left_to_element(L.TXT_DURATION_OPTION.format(duration), L.EL_DURATION_STRIP)

    def scroll_to_schedule(self):
        self.capture_step("scroll_to_schedule")
        self.scroll_to(L.TXT_DURATION_TITLE)

    def scroll_to_location(self):
        self.capture_step("scroll_to_location")
        self.scroll_to(L.BTN_GOOGLE_MAPS)

    def scroll_to_more_information(self):
        self.capture_step("scroll_to_more_information")
        self.scroll_to(L.TXT_MORE_INFORMATION)

    def open_maps(self):
        self.capture_step("open_maps")
        self.scroll_and_click(L.BTN_GOOGLE_MAPS)

    def open_pricelist(self):
        self.capture_step("open_pricelist")
        self.scroll_and_click(L.BTN_SEE_PRICELIST)

    def tap_show_more(self):
        self.capture_step("tap_show_more")
        self.scroll_and_click(L.BTN_SHOW_MORE)

    def tap_book(self):
        self.capture_step("tap_book")
        self.click(L.BTN_BOOK)

    def tap_back(self):
        self.capture_step("tap_back")
        self.click(L.BTN_BACK)

    def venue_name_text(self, name):
        return self.label_of(L.TXT_VENUE_NAME.format(name))

    def location_text(self):
        return self.label_of(L.TXT_LOCATION)

    def distance_text(self):
        return self.label_of(L.TXT_DISTANCE)

    def address_text(self):
        return self.label_of(L.TXT_ADDRESS)

    def distance_from_location_text(self):
        return self.label_of(L.TXT_DISTANCE_FROM_LOCATION)

    def description_text(self):
        return self.label_of(L.TXT_DESCRIPTION)

    def promo_items(self):
        return self.texts_of(L.LIST_PROMOS)

    def date_items(self):
        return self.texts_of(L.LIST_DATE_STRIP)

    def time_slot_items(self):
        return self.texts_of(L.LIST_TIME_SLOTS)

    def duration_items(self):
        return self.texts_of(L.LIST_DURATIONS)

    def has_map(self, timeout=5):
        return self.is_visible(L.EL_MAP, timeout)

    def rate_text(self, duration):
        return self.label_of(L.IMG_RATE_BY_DURATION.format(duration))

    def has_time(self, time, timeout=5):
        return self.is_visible(L.TXT_TIME_SLOT.format(time), timeout)

    def has_duration(self, duration, timeout=5):
        return self.is_visible(L.TXT_DURATION_OPTION.format(duration), timeout)

    def book_is_enabled(self):
        return self.is_enabled(L.BTN_BOOK)
