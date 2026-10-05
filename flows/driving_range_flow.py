from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from pages.homepage.home_page import HomePage
from pages.driving_range.driving_range_list_page import DrivingRangeListPage
from pages.driving_range.driving_range_search_page import DrivingRangeSearchPage
from pages.driving_range.driving_range_details_page import DrivingRangeDetailsPage
from pages.driving_range.featured_promos_page import FeaturedPromosPage
from pages.driving_range.date_picker_page import DatePickerPage
from pages.driving_range.bay_picker_page import BayPickerPage
from pages.driving_range.booking_confirmation_page import BookingConfirmationPage
from pages.driving_range.available_promos_page import AvailablePromosPage
from pages.driving_range.add_promo_code_page import AddPromoCodePage
from pages.payment_method_page import PaymentMethodPage
from pages.payment_gateway_page import PaymentGatewayPage
from pages.driving_range.booking_success_page import BookingSuccessPage
from pages.driving_range.dr_booking_details_page import DrBookingDetailsPage
from pages.swing_credits.swing_credits_page import SwingCreditsPage
from pages.swing_credits.credits_history_page import CreditsHistoryPage
from pages.add_credit_card_page import AddCreditCardPage
from pages.card_linked_success_page import CardLinkedSuccessPage
from pages.confirm_credit_card_page import ConfirmCreditCardPage
from pages.purchase_authentication_page import PurchaseAuthenticationPage
from helpers import amounts


class DrivingRangeFlow(BaseFlow):

    FLOW_NAME = "DrivingRangeFlow"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.list = self.page(DrivingRangeListPage)
        self.search = self.page(DrivingRangeSearchPage)
        self.details = self.page(DrivingRangeDetailsPage)
        self.featured = self.page(FeaturedPromosPage)
        self.calendar = self.page(DatePickerPage)
        self.bays = self.page(BayPickerPage)
        self.confirm = self.page(BookingConfirmationPage)
        self.promos = self.page(AvailablePromosPage)
        self.promo_code = self.page(AddPromoCodePage)
        self.payment = self.page(PaymentMethodPage)
        self.gateway = self.page(PaymentGatewayPage)
        self.success = self.page(BookingSuccessPage)
        self.booking = self.page(DrBookingDetailsPage)
        self.credits = self.page(SwingCreditsPage)
        self.history = self.page(CreditsHistoryPage)
        self.credit_card = self.page(AddCreditCardPage)
        self.authentication = self.page(PurchaseAuthenticationPage)
        self.card_linked = self.page(CardLinkedSuccessPage)
        self.confirm_card = self.page(ConfirmCreditCardPage)

    # ----------------------------- actions -----------------------------

    def open_home_tab(self):
        self.home.open_home_tab()
        

    def open_driving_range(self, member_type = ""):
        self.home.open_driving_range()
        self.list.verify_screen(member_type)
    

    def open_swing_credits(self):
        self.home.wait_until_loaded()
        self.home.open_credits()
        self.credits.verify_screen()
    

    def open_swing_credit_history(self):
        self.credits.open_history()
        self.history.verify_screen()
    

    def only_swing_pass_partners(self, member_type = ""):
        self.list.scroll_to_swing_pass_filter()
        self.list.enable_swing_pass_filter()
        self.list.verify_screen(member_type)

    def all_partners(self, member_type = ""):
        self.list.scroll_to_swing_pass_filter()
        self.list.disable_swing_pass_filter()
        self.list.verify_screen(member_type)

    def open_search(self):
        self.list.open_search()
        self.search.verify_screen()

    def search_driving_range(self, name):
        self.search.enter_search(name)
        self.search.submit_search()
        self.search.verify_result_search(name)

    def open_result(self, name):
        self.search.open_result(name)
        self.details.verify_screen()

    def see_all_details_sections(self):
        self.details.verify_all_sections()

    def open_featured_promos(self):
        self.details.open_featured_promos()
        self.featured.verify_screen()

    def find_featured_promo(self, name):
        self.featured.scroll_to_promo(name)

    def open_featured_promo(self, name):
        self.featured.open_promo(name)

    def back_to_details(self):
        self.featured.tap_back()
        self.details.verify_screen()

    def open_calendar(self):
        self.details.open_date_picker()
        self.calendar.verify_screen()

    def choose_date(self, label):
        self.calendar.select_day(label)

    def choose_bay_type(self, name):
        if name:
            self.details.select_bay_type(name)

    def choose_time(self, time, time_end=None):
        self.details.select_time(time, time_end)

    def choose_duration(self, duration):
        self.details.select_duration(duration)

    def book_driving_range(self):
        self.details.tap_book()
        self.bays.verify_screen()

    def add_bay(self):
        self.bays.increase_bays()

    def set_bays(self, count):
        self.bays.set_bays(count)

    def confirm_bays(self):
        self.bays.tap_confirm()
        self.confirm.verify_screen()

    def add_addons(self, addons):
        self.confirm.set_items(addons)

    def set_balls(self, option, count):
        self.confirm.set_balls(option, count)
    

    def set_items(self, items):
        if items:
            self.confirm.set_items(items)

    def add_balls(self, option):
        self.confirm.add_balls(option)

    def set_addon(self, name, count):
        self.confirm.set_addon(name, count)

    def add_addon(self, name):
        self.confirm.add_addon(name)

    def remove_addon(self, name):
        self.confirm.remove_addon(name)

    def enter_note(self, text):
        self.confirm.enter_note(text)

    def use_swing_credits(self):
        self.confirm.toggle_swing_credits()

    def open_promos(self):
        self.confirm.open_promos()
        self.promos.verify_screen()

    def remove_promo(self):
        if self.confirm.get_promo_in_btn_promo() != "Apply promo":
            self.open_promos()
            self.promos.remove_promo()
            self.promos.tap_back()

    def apply_promo(self, promo_name):
        if promo_name not in self.confirm.get_promo_in_btn_promo():
            self.open_promos()
            self.promos.enter_search(promo_name)
            self.promos.apply_promo(promo_name)
    

    def apply_and_redeem_promo(self, promo_name, promo_code):
        self.open_promos()
        self.open_promo_code()
        self.apply_promo_code(promo_code)
        self.promos.enter_search(promo_name)
        self.promos.apply_promo(promo_name)

    def open_promo_code(self):
        self.promos.open_add_promo_code()
        self.promo_code.verify_screen()

    def apply_promo_code(self, code):
        self.promo_code.enter_promo_code(code)
        self.promo_code.tap_add()

    def back_to_confirmation(self):
        self.promos.tap_back()
        self.confirm.verify_screen()

    def choose_payment_method(self, name):
        self.confirm.open_payment_method()
        self.payment.verify_screen()
        self.payment.select_method(name)

    def pay_now(self):
        self.confirm.tap_pay_now()
        self.proceed_to_pay()

    def proceed_to_pay(self):
        self.gateway.tap_proceed_to_pay()

    def open_booking_details(self):
        self.success.open_booking_details()
        self.booking.verify_screen()
    

    def back_to_activity(self):
        self.booking.tap_back()
        
    

    def get_payment_information_before_payment(self, used_credit = "0"):
        return self.confirm.payment_information(used_credit)

    def get_booking_code_after_payment(self):
        return self.success.booking_code_text()
    
    def add_new_credit_card(self, card_name, card_number, card_expiry_date, card_cvv, is_primary: bool):
        self.confirm.open_payment_method()
        self.payment.add_credit_card()
        self.credit_card.enter_cardholder_name(card_name)
        self.credit_card.enter_card_number(card_number)
        self.credit_card.enter_expiry_date(card_expiry_date)
        self.credit_card.enter_cvv(card_cvv)
        if is_primary:
            self.credit_card.toggle_primary_method()
        self.credit_card.tap_save_credit_card()
    

    def link_new_credit_card(self, card_name, card_number, card_expiry, card_cvv, otp):
        self.confirm.open_payment_method()
        self.payment.verify_screen()
        self.payment.add_credit_card()
        self.credit_card.verify_screen()
        self.credit_card.enter_cardholder_name(card_name)
        self.credit_card.enter_card_number(card_number)
        self.credit_card.enter_expiry_date(card_expiry)
        self.credit_card.enter_cvv(card_cvv)
        self.credit_card.tap_save_credit_card()
        self.authenticate_card(otp)
        self.card_linked.verify_screen()
        self.card_linked.tap_close()
        self.confirm.verify_screen()

    def authenticate_card(self, otp):
        self.authentication.verify_screen()
        self.authentication.enter_otp_code(otp)
        self.authentication.tap_submit()

    def pay_now_with_credit_card(self, card_cvv, otp):
        self.confirm.tap_pay_now()
        self.confirm_card.verify_screen()
        self.confirm_card.enter_cvv(card_cvv)
        self.confirm_card.tap_confirm()
        if self.authentication.is_loaded(15):
            self.authenticate_card(otp)

    # --------------------------- verifications ---------------------------

    def verify_earn_credit_booking_code(self, booking_code: str, total_amount):
        self.history.open_earned_tab()
        self.history.verify_credit_by_booking_code(booking_code)
        table = CheckTable(f"Swing Credits earned for {amounts.booking_tag(booking_code)}")
        table.amount("Credits earned", total_amount, self.history.booking_amount_number(booking_code))
        table.verify()

    def verify_booking_confirmation(self):
        self.confirm.verify_screen()

    def verify_payment_success(self):
        self.success.verify_screen()

    def verify_button_exclusive_featured_promo(self, member_type):
        self.details.verify_exclusive_swing_pass_promo(member_type)
    

    def verify_maximum_bays_driving_range(self, tot_bays):
        self.bays.set_bays(tot_bays)
        self.bays.verify_maximum_bays(tot_bays)
    

    def verify_maximum_balls(self):
        table = CheckTable("Maximum balls")
        disabled = self.confirm.button_balls_increase_is_disabled("balls")
        table.add("Increase button", "disabled", "disabled" if disabled else "enabled", disabled)
        table.verify()

    def verify_minimum_balls(self):
        table = CheckTable("Minimum balls")
        shown = self.confirm.is_visible_minimum_toaster()
        table.add("Minimum balls toaster", "shown", "shown" if shown else "not shown", shown)
        table.verify()

    def verify_auto_applied_promo(self, promo_name):
        promo = self.confirm.get_promo_in_btn_promo()
        table = CheckTable("Auto applied promo")
        table.contains("Promo name", promo_name, promo)
        table.contains("Promo state", "promo auto applied!", promo)
        table.verify()

    def verify_booking_information(self, player_name, date, start_time, end_time, bay_type: str = ""):
        table = CheckTable("Booking confirmation")
        table.equal("Player name", player_name, self.confirm.player_name_text())
        table.contains("Booking date", date, self.confirm.booking_date_text())
        table.contains("Booking time", start_time, self.confirm.booking_time_text())
        table.contains("Duration", self.confirm.get_duration(start_time, end_time), self.confirm.duration_text())
        if bay_type:
            table.equal("Bay type", bay_type, self.confirm.bay_type_text())
        table.verify()

    def verify_payment_success_driving_range(self, player_name, date, start_time, end_time, number_of_bay, payment_information, bay_type=""):
        table = CheckTable("Payment successful")
        table.equal("Player name", player_name, self.success.player_name_text())
        table.contains("Booking date", date, self.success.booking_date_text())
        table.contains("Booking time", start_time, self.success.booking_time_text())
        table.contains("Duration", self.confirm.get_duration(start_time, end_time), self.success.duration_text())
        table.contains("No. of bays", number_of_bay, self.success.number_of_bays_text())
        if bay_type:
            table.equal("Bay type", bay_type, self.success.bay_type_text())
        table.amount("Total payment", payment_information["total_payment"], self.success.total_payment_text())
        if payment_information["earned_credit"]:
            table.amount("Swing Credits earned", payment_information["earned_credit"],
                         self.success.earned_credits_text())
        table.verify()

    def verify_data_booking_details_with_credit_used(self, booking_code, player_name, date, start_time, end_time, number_of_bay, payment_information, bay_type=""):
        table = self.booking_details_table(booking_code, player_name, date, start_time, end_time,
                                           number_of_bay, payment_information, bay_type)
        table.amount("Swing Credits used", payment_information["used_credit"], self.booking.used_credit_text())
        table.verify()

    def booking_details_table(self, booking_code, player_name, date, start_time, end_time, number_of_bay, payment_information, bay_type=""):
        table = CheckTable("Booking details")
        table.contains("Booking code", amounts.booking_tag(booking_code), self.booking.booking_code_text())
        table.equal("Player name", player_name, self.booking.player_name_text())
        table.contains("Booking date", date, self.booking.booking_date_text())
        table.contains("Booking time", start_time, self.booking.booking_time_text())
        table.contains("Duration", self.confirm.get_duration(start_time, end_time), self.booking.duration_text())
        table.contains("No. of bays", number_of_bay, self.booking.number_of_bays_text())
        if bay_type:
            table.equal("Bay type", bay_type, self.booking.bay_type_text())
        table.amount("Total payment", payment_information["total_payment"], self.booking.total_payment_text())
        if payment_information["earned_credit"]:
            table.amount("Swing Credits earned", payment_information["earned_credit"],
                         self.booking.earned_credits_text())
        return table

    def verify_data_booking_details_without_credit_used(self, booking_code, player_name, date, start_time, end_time, number_of_bay, payment_information, bay_type=""):
        self.booking_details_table(booking_code, player_name, date, start_time, end_time,
                                   number_of_bay, payment_information, bay_type).verify()

    def verify_used_credit_booking_code(self, booking_code, total_amount):
        self.history.open_usage_tab()
        self.history.verify_credit_by_booking_code(booking_code)
        table = CheckTable(f"Swing Credits used for {amounts.booking_tag(booking_code)}")
        table.amount("Credits used", total_amount, self.history.booking_amount_number(booking_code))
        table.verify()
    
    
