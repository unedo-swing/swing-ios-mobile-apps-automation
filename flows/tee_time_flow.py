from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from pages.homepage.home_page import HomePage
from pages.tee_time.tee_time_list_page import TeeTimeListPage
from pages.tee_time.tee_time_search_page import TeeTimeSearchPage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage
from pages.tee_time.featured_promos_page import TeeTimeFeaturedPromosPage
from pages.tee_time.booking_method_page import BookingMethodPage
from pages.tee_time.booking_confirmation_page import TeeTimeBookingConfirmationPage
from pages.tee_time.available_promos_page import TeeTimeAvailablePromosPage
from pages.driving_range.add_promo_code_page import AddPromoCodePage
from pages.tee_time.add_ons_page import AddOnsPage
from pages.tee_time.add_player_page import AddPlayerPage
from pages.country_picker_page import CountryPickerPage
from pages.tee_time.group_booking_info_page import GroupBookingInfoPage
from pages.payment_method_page import PaymentMethodPage
from pages.payment_gateway_page import PaymentGatewayPage
from pages.tee_time.booking_success_page import TeeTimeBookingSuccessPage
from pages.tee_time.tt_booking_details_page import TeeTimeBookingDetailsPage
from pages.tee_time.booking_summary_page import TeeTimeBookingSummaryPage
from pages.tee_time.credits_earnings_page import TeeTimeCreditsEarningsPage
from pages.swing_credits.swing_credits_page import SwingCreditsPage
from pages.swing_credits.credits_history_page import CreditsHistoryPage
from pages.add_credit_card_page import AddCreditCardPage
from pages.card_linked_success_page import CardLinkedSuccessPage
from pages.confirm_credit_card_page import ConfirmCreditCardPage
from pages.purchase_authentication_page import PurchaseAuthenticationPage
from helpers import amounts


class TeeTimeFlow(BaseFlow):
    FLOW_NAME = "TeeTimeFlow"
    APPLY_PROMO_LABEL = "Apply a promo"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.list = self.page(TeeTimeListPage)
        self.search = self.page(TeeTimeSearchPage)
        self.details = self.page(GolfCourseDetailsPage)
        self.featured = self.page(TeeTimeFeaturedPromosPage)
        self.method = self.page(BookingMethodPage)
        self.confirm = self.page(TeeTimeBookingConfirmationPage)
        self.promos = self.page(TeeTimeAvailablePromosPage)
        self.promo_code = self.page(AddPromoCodePage)
        self.addons = self.page(AddOnsPage)
        self.player = self.page(AddPlayerPage)
        self.country = self.page(CountryPickerPage)
        self.group_info = self.page(GroupBookingInfoPage)
        self.payment = self.page(PaymentMethodPage)
        self.gateway = self.page(PaymentGatewayPage)
        self.success = self.page(TeeTimeBookingSuccessPage)
        self.booking = self.page(TeeTimeBookingDetailsPage)
        self.credits = self.page(TeeTimeCreditsEarningsPage)
        self.summary = self.page(TeeTimeBookingSummaryPage)
        self.credits_history = self.page(SwingCreditsPage)
        self.history = self.page(CreditsHistoryPage)
        self.credit_card = self.page(AddCreditCardPage)
        self.authentication = self.page(PurchaseAuthenticationPage)
        self.card_linked = self.page(CardLinkedSuccessPage)
        self.confirm_card = self.page(ConfirmCreditCardPage)
    
    def open_home_tab(self):
        self.home.open_home_tab()
    
    def open_swing_credits(self):
        self.home.wait_until_loaded()
        self.home.open_credits()
        self.credits_history.verify_screen()
    
    def open_swing_credit_history(self):
        self.credits_history.open_history()
        self.history.verify_screen()

    def open_tee_time(self, member_type=""):
        self.home.open_tee_time()
        self.list.verify_screen(member_type)

    def only_swing_pass_partners(self, member_type="swing-pass"):
        self.list.scroll_to_swing_pass_filter()
        self.list.enable_swing_pass_filter()
        self.list.verify_screen(member_type)

    def all_partners(self, member_type=""):
        self.list.scroll_to_swing_pass_filter()
        self.list.disable_swing_pass_filter()
        self.list.verify_screen(member_type)

    def find_golf_course(self, text):
        self.list.scroll_to_card(text)

    def open_golf_course(self, text):
        self.list.open_card(text)
        self.details.verify_screen()

    def open_search(self):
        self.list.open_search()
        self.search.verify_screen()

    def search_golf_course(self, name):
        self.search.search(name)
        self.search.submit_search()

    def open_result(self, name):
        self.search.open_result(name)
        self.details.verify_screen()

    def open_recent_search(self, name):
        self.search.open_recent_search(name)

    def open_featured_promos(self):
        self.details.open_featured_promos()
        self.featured.verify_screen()

    def find_featured_promo(self, name):
        self.featured.scroll_to_promo(name)

    def back_to_details(self):
        self.featured.tap_back()
        self.details.verify_screen()

    def choose_date(self, label):
        self.details.open_calendar()
        self.details.select_date(label)

    def choose_session(self, name = ""):
        self.details.select_session(name)

    def choose_tee_time(self, time):
        self.details.select_slot(time)
        
    def see_all_details_sections(self):
        self.details.verify_all_sections()

    def find_date(self, label):
        self.details.swipe_to_date(label)

    def find_promo_on_details(self, name):
        self.details.swipe_to_promo(name)

    def see_course_information(self):
        self.details.show_more_information()

    def book_tee_time(self):
        self.details.tap_book_tee_time()
        self.method.verify_screen()

    def choose_standard_booking(self):
        self.method.choose_standard_booking()
        self.confirm.verify_screen()

    def choose_group_booking(self):
        self.method.choose_group_booking()
        self.confirm.verify_screen()

    def open_booking_method(self):
        self.confirm.open_booking_method()
        self.method.verify_screen()

    def switch_to_group_booking(self):
        self.group_info.switch_to_group_booking()
        self.confirm.verify_screen()

    def close_group_booking_info(self):
        self.group_info.tap_close()
        self.confirm.verify_screen()

    def close_group_booking_info_if_shown(self):
        if self.group_info.has_close_button():
            self.group_info.tap_close()

    def open_promos(self, player):
        self.confirm.open_promos(player)
        self.promos.verify_screen()

    def find_promo(self, name):
        self.promos.search_promo(name)

    def apply_promo(self):
        self.promos.apply_promo()

    def apply_player_promo(self, player, promo_name):
        self.open_promos(player)
        self.find_promo(promo_name)
        self.apply_promo()

    def apply_player_promos(self, players):
        for player in players or []:
            if player.get("promo_name") and not player.get("promo_code"):
                self.apply_player_promo(player["player"], player["promo_name"])

    def redeem_player_promo(self, player, promo_name, promo_code):
        self.open_promos(player)
        self.open_promo_code()
        self.apply_promo_code(promo_code)
        self.find_promo(promo_name)
        self.apply_promo()


    def remove_promo(self, player_name):
        self.open_promos(player_name)
        self.promos.remove_promo()
        self.promos.tap_back()

    def remove_player_promo(self, player):
        self.open_promos(player)
        self.promos.remove_promo()
        self.promos.tap_back()

    def verify_promo_removed(self, player):
        text = self.confirm.player_promo_text(player)
        assert self.APPLY_PROMO_LABEL in text, ( # type: ignore
            f"{player} still has a promo applied: "
            f"expected {self.APPLY_PROMO_LABEL!r}, found {text!r}")
    
    def verify_promo_applied(self, player, promo_name):
        text = self.confirm.player_promo_text(player)
        assert promo_name in text, ( # type: ignore
            f"{player} still has a promo applied: "
            f"expected {promo_name!r}, found {text!r}")
    
    def verify_promo_autoapplied(self, player, promo_name):
        text = self.confirm.player_promo_text(player)
        assert promo_name in text, ( # type: ignore
            f"{player} still has a promo applied: "
            f"expected {promo_name!r}, found {text!r}")

    def remove_promo_and_verify(self, player):
        self.remove_player_promo(player)
        self.verify_promo_removed(player)

    def remove_players_promos(self, players, host=""):
        for player in self.payment_player_names(players, host):
            self.remove_player_promo(player)

    def open_promo_code(self):
        self.promos.open_add_promo_code()
        self.promo_code.verify_screen()

    def apply_promo_code(self, code):
        self.promo_code.enter_promo_code(code)
        self.promo_code.tap_add()

    def back_to_confirmation(self):
        self.promos.tap_back()
        self.confirm.verify_screen()

    def open_addons(self, player):
        self.confirm.open_addons(player)
        self.addons.verify_screen()

    def add_addon(self, name):
        self.addons.add_item(name)

    def remove_addon(self, name):
        self.addons.remove_item(name)

    def save_addons(self):
        self.addons.tap_save()
        self.confirm.verify_screen()

    def set_player_addons(self, player, name, quantity=1):
        self.open_addons(player)
        for _ in range(int(quantity or 1)):
            self.add_addon(name)
        self.save_addons()

    def add_players_addons(self, players):
        for player in players or []:
            if player.get("add_ons_name"):
                self.set_player_addons(player["player"], player["add_ons_name"],
                                       player.get("add_ons_qty", 1))

    def cancel_addons(self):
        self.addons.tap_cancel()
        self.confirm.verify_screen()

    def use_players_swing_credits(self, players, host=""):
        for player in self.payment_player_names(players, host):
            self.use_swing_credits(player)

    def use_swing_credits(self, player_name):
        self.confirm.toggle_swing_credits(player_name)

    def enter_note(self, text):
        self.confirm.enter_note(text)

    def add_player(self):
        self.confirm.add_player()
        self.player.verify_screen()

    def search_friend(self, name):
        self.player.search_friend(name)

    def select_friend(self, username):
        self.player.select_friend(username)
        self.close_group_booking_info_if_shown()
        self.confirm.verify_screen()

    def open_add_manually(self):
        self.player.open_add_manually_tab()

    def fill_player(self, first_name, last_name, phone_number):
        self.player.enter_first_name(first_name)
        self.player.enter_last_name(last_name)
        self.player.enter_phone_number(phone_number)

    def enter_player_email(self, email):
        self.player.enter_email(email)

    def open_player_country_picker(self):
        self.player.open_country_picker()
        self.country.verify_screen()

    def choose_player_country(self, name):
        self.country.select_country(name)
        self.player.verify_screen()

    def save_player(self):
        self.player.tap_save_player()
        self.close_group_booking_info_if_shown()
        self.confirm.verify_screen()

    def remove_player(self, player):
        self.confirm.remove_player(player)

    def open_payment_method(self):
        self.confirm.change_payment_method()
        self.payment.verify_screen()

    def choose_payment_method(self, name):
        self.confirm.change_payment_method()
        self.payment.verify_screen()
        self.payment.select_method(name)
        self.confirm.verify_screen()

    def invite_player(self, player):
        self.add_player()
        if str(player.get("add_method", "search")).lower() == "manual":
            self.open_add_manually()
            self.fill_player(player.get("first_name"), player.get("last_name"),
                             player.get("phone_number"))
            self.save_player()
        else:
            self.search_friend(player.get("search_keyword") or player.get("username"))
            self.select_friend(player.get("username"))

    def invite_players(self, players, total_players=""):
        for player in self.players_to_invite(players, total_players):
            self.invite_player(player)

    def verify_player_added(self, player):
        assert self.confirm.has_player(player), (
            f"{player} was not added to the booking, "
            f"the confirmation shows {self.confirm.player_count()} players")

    def verify_players_added(self, players, host=""):
        for player in self.payment_player_names(players, host):
            self.verify_player_added(player)

    def invite_players_and_remove_promos(self, players, total_players=""):
        for player in self.players_to_invite(players, total_players):
            self.invite_player(player)
            self.verify_player_added(player["player"])
            self.remove_promo_and_verify(player["player"])
    
    def invite_players_only_with_autoapplied_promo(self, players, total_players=""):
        for player in self.players_to_invite(players, total_players):
            self.invite_player(player)
            self.verify_player_added(player["player"])
            self.verify_promo_autoapplied(player["player"], player["promo_name"])
    
    def invite_players_and_redeemed_promos(self, players, total_players=""):
        for player in self.players_to_invite(players, total_players):
            self.invite_player(player)
            self.verify_player_added(player["player"])
            self.redeem_player_promo(player["player"], player["promo_name"], player["promo_code"])
            self.verify_promo_applied(player["player"], player["promo_name"])

    def verify_booking_information(self, date, session, preferred_time, booking_type, players):
        
        assert date in self.confirm.booking_date_text(), (f"booking date text does not contain date: expected {date}, found {self.confirm.booking_date_text()}")
        assert session in self.confirm.session_text(), (f"session text does not contain session: expected {session}, found {self.confirm.session_text()}")
        assert preferred_time in self.confirm.preferred_time_text(), (f"preferred time text does not contain preferred time: expected {preferred_time}, found {self.confirm.preferred_time_text()}")
        assert booking_type in self.confirm.booking_type_text(), (f"booking type text does not contain booking type: expected {booking_type}, found {self.confirm.booking_type_text()}")
        for player in players or []:
            assert self.confirm.has_player(player["player"]), f"{player['player']} not in the booking"

    def verify_player_promo(self, player, promo_name):
        assert promo_name in self.confirm.player_promo_text(player), (f"player promo text(player) does not contain promo name: expected {promo_name}, found {self.confirm.player_promo_text(player)}")
    
    def verify_host_auto_applied_promo(self, player, promo_name):
        assert promo_name in self.confirm.player_promo_text(player), (f"player promo text(player) does not contain promo name: expected {promo_name}, found {self.confirm.player_promo_text(player)}")

    def verify_player_without_promo(self, player, promo_names=()):
        text = self.confirm.player_promo_text(player)
        for name in promo_names or ():
            assert name not in text, f"{player} should not use the promo {name}"

    def verify_players_promos(self, players):
        names = [player["promo_name"] for player in players or [] if player.get("promo_name")]
        for player in players or []:
            if player.get("promo_name"):
                self.verify_player_promo(player["player"], player["promo_name"])
            else:
                self.verify_player_without_promo(player["player"], names)

    def verify_auto_applied_promos(self, players, promo_name=""):
        for player in self.player_names(players):
            text = self.confirm.player_promo_text(player)
            assert promo_name in text if promo_name else "auto applied" in text.lower(), (f"{player} does not show an auto applied promo") # type: ignore
            
    def verify_auto_applied_promos_host(self, host_name, promo_name=""):
        text = self.confirm.player_promo_text(host_name)
        assert promo_name in text if promo_name else "auto applied" in text.lower(), (f"{host_name} does not show an auto applied promo") # type: ignore
            

    def verify_players_without_promo(self, players, promo_names=()):
        for player in self.player_names(players):
            self.verify_player_without_promo(player, promo_names)

    def apply_promo_for(self, player, promo_name):
        self.apply_player_promo(player, promo_name)

    def verify_player_addons(self, player, name):
        assert name in self.confirm.player_addons_text(player), (f"player addons text(player) does not contain name: expected {name}, found {self.confirm.player_addons_text(player)}")

    def open_price_details(self):
        self.confirm.scroll_to_price_details()

    def get_payment_information_before_payment(self, used_credit="0", players=None, host=""):
        self.open_price_details()
        return self.confirm.payment_information(used_credit, self.payment_player_names(players, host))

    def payment_players(self, payment_information):
        return list((payment_information or {}).get("players") or {})

    def payment_players_count(self, payment_information):
        return len(self.payment_players(payment_information))

    def verify_payment_success_payment_information(self, date, session, preferred_time,
                                                   payment_information, venue="", payment_method=""):
        self.verify_payment_success_tee_time(date, session, preferred_time, payment_information, venue, payment_method, str(self.payment_players_count(payment_information))) # type: ignore

    def verify_booking_details_payment_information(self, booking_code, date, session, preferred_time,
                                                   payment_information, status="UPCOMING"):
        self.verify_data_booking_details(
            booking_code, date, session, preferred_time, payment_information,
            str(self.payment_players_count(payment_information)), status)

    def verify_payment_information(self, payment_information, players=None, host=""):
        lines = payment_information.get("players") or {}
        table = CheckTable("Price details")
        for player in self.payment_player_names(players, host):
            table.truthy(f"{player} - price line", lines.get(player, {}).get("price_line", ""))
            table.truthy(f"{player} - publish rate", lines.get(player, {}).get("publish_rate", ""))
        table.truthy("Total payment", payment_information.get("total_payment"))
        table.verify()

    def verify_player_used_credits(self, player, expected_amount):
        used = self.confirm.player_used_credits(player)
        expected = abs(amounts.to_number(expected_amount))
        assert used == expected, (
            f"swing credits used for {player} do not match: expected {expected}, found {used}")

    def used_credits_applied(self, payment_information):
        return bool(amounts.to_number((payment_information or {}).get("used_credit", "")))

    def verify_players_used_credits(self, payment_information, players=None, host=""):
        if not self.used_credits_applied(payment_information):
            self.log.info("swing credits were not used on this booking, skipping the credits check")
            return
        lines = payment_information.get("players") or {}
        names = self.payment_player_names(players, host) or list(lines)
        for player in names:
            assert self.confirm.has_player_used_credits(player), (
                f"{player} does not show a swing credits used line")
        table = CheckTable("Swing Credits used")
        for player in names:
            table.truthy(f"{player} - credits line", lines.get(player, {}).get("used_credit", ""))
        used = sum(abs(amounts.to_number(lines.get(player, {}).get("used_credit", "")))
                   for player in names)
        table.amount("Credits total", payment_information.get("used_credit", ""), used)
        table.verify()

    def get_booking_code_after_payment(self):
        return self.success.booking_code_text()

    def verify_payment_success_tee_time(self, date, session, preferred_time, payment_information, venue="", payment_method="", player=1):
        self.success.verify_screen()
        table = CheckTable("Payment successful")
        table.truthy("Booking code", self.success.booking_code_text())
        table.contains("Booking date", date, self.success.booking_date_text())
        if session:
            table.contains("Session", session, self.success.session_text())
        table.contains("Preferred time", preferred_time, self.success.preferred_time_text())
        table.contains("No. of players", player, self.success.players_text())
        table.amount("Total payment", payment_information["total_payment"], self.success.total_text())
        if venue:
            table.contains("Venue", venue, self.success.venue_text())
        if payment_method:
            table.contains("Payment method", payment_method, self.success.payment_method_text())
        if payment_information.get("earned_credit"):
            table.amount("Swing Credits earned", payment_information["earned_credit"],
                         self.success.earned_credits_text())
        table.verify()

    def verify_data_booking_details(self, booking_code, date, session, preferred_time,
                                    payment_information, player="1", status="UPCOMING"):
        self.booking.verify_screen()
        table = CheckTable("Booking details")
        table.contains("Booking code", amounts.booking_tag(booking_code), self.booking.booking_code_text())
        table.contains("Booking date", date, self.booking.booking_date_text())
        if session:
            table.contains("Session", session, self.booking.session_text())
        table.contains("Preferred time", preferred_time, self.booking.preferred_time_text())
        table.contains("No. of players", player, self.booking.players_text())
        table.amount("Total payment", payment_information["total_payment"], self.booking.total_payment_text())
        if status:
            table.add("Status", status, status if self.booking.has_status(status) else "not shown",
                      self.booking.has_status(status))
        if payment_information.get("earned_credit"):
            table.amount("Swing Credits earned", payment_information["earned_credit"],
                         self.booking.earned_credits_text())
        table.verify()

    def get_booking_details_information(self):
        return self.booking.payment_information()

    def pay_now(self):
        self.confirm.tap_pay_now()
        self.proceed_to_pay()

    def proceed_to_pay(self):
        self.gateway.tap_proceed_to_pay()

    def link_new_credit_card(self, card_name, card_number, card_expiry, card_cvv, otp):
        self.confirm.change_payment_method()
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

    def verify_payment_success(self):
        self.success.verify_screen()

    def finish(self):
        self.success.tap_finish()

    def open_booking_details(self):
        self.success.open_booking_details()
        self.booking.verify_screen()

    def open_complete_breakdown(self):
        self.booking.open_breakdown()
        self.summary.verify_screen()

    def back_to_booking_details(self):
        self.summary.tap_back()
        self.booking.verify_screen()
    
    def back_to_activity(self):
        self.booking.tap_back()
    
    def verify_button_exclusive_featured_promo(self, player_type):
        self.details.verify_exclusive_swing_pass_promo(player_type)
    
    def verify_confirmation_player(self, player):
        name = player["player"] if isinstance(player, dict) else str(player)
        self.confirm.scroll_to_player(name)
        assert self.confirm.has_player(name), f"{name} not in the booking"
        self.confirm.scroll_to_player_price_line(name)
        assert self.confirm.price_line_text(name), f"price detail line missing for {name}"
        if isinstance(player, dict) and player.get("promo_name"):
            assert player["promo_name"] in self.confirm.player_promo_text(name), (
                f"{name} does not show the promo: expected "
                f"{player['promo_name']}, found {self.confirm.player_promo_text(name)}")
        if isinstance(player, dict) and player.get("add_ons_name"):
            assert player["add_ons_name"] in self.confirm.player_addons_text(name), (
                f"{name} does not show the add on: expected "
                f"{player['add_ons_name']}, found {self.confirm.player_addons_text(name)}")
    

    def verify_payment_success_players(self, date, session, preferred_time, payment_information,
                                       players, venue="", payment_method=""):
        self.verify_payment_success_tee_time(date, session, preferred_time, payment_information,
                                             venue, payment_method, str(self.player_total(players))) # type: ignore

    def verify_booking_details_players(self, booking_code, date, session, preferred_time,
                                       payment_information, players, status="UPCOMING"):
        self.verify_data_booking_details(booking_code, date, session, preferred_time,
                                         payment_information, str(self.player_total(players)), status)

    def open_credits_earnings(self):
        self.confirm.open_credits_earnings()
        self.credits.verify_screen()

    def verify_credits_earnings_players(self, players):
        self.credits.verify_screen()
        for player in players or []:
            assert self.credits.has_earning(player["player"]), (
                f"credits earning row missing for {player['player']}")

    def close_credits_earnings(self):
        self.credits.tap_got_it()
        self.confirm.verify_screen()

    def verify_booking_confirmation(self, booking_date, session, prefereed_time, method_booking, total_players):
        self.confirm.go_to_top()
        table = CheckTable("Booking confirmation")
        table.equal("Booking date", booking_date, self.confirm.booking_date_text())
        table.equal("Session", session, self.confirm.session_text())
        table.equal("Preferred time", prefereed_time, self.confirm.preferred_time_text())
        table.equal("No. of players", self.player_number(total_players), self.confirm.player_count())
        table.equal("Booking method", method_booking, self.confirm.booking_type_text())
        table.verify()

    def verify_used_credit_booking_code(self, booking_code, total_amount):
        self.history.open_usage_tab()
        self.history.verify_credit_by_booking_code(booking_code)
        used = abs(self.history.booking_amount_number(booking_code))
        expected = abs(amounts.to_number(total_amount))
        assert used == expected, (
            f"used credits for {amounts.booking_tag(booking_code)} do not match: "
            f"expected {expected}, found {used}")

    def verify_used_credit_by_player(self, booking_code, player, expected_amount):
        self.history.scroll_to_booking_player(booking_code, player)
        self.history.verify_credit_by_booking_code_player(booking_code, player)
        used = abs(self.history.booking_amount_number_for_player(booking_code, player))
        expected = abs(amounts.to_number(expected_amount))
        assert used == expected, (
            f"used credits for {amounts.booking_tag(booking_code)} and {player} do not match: "
            f"expected {expected}, found {used}")

    def verify_used_credit_booking_code_players(self, booking_code, payment_information,
                                                players=None, host=""):
        if not self.used_credits_applied(payment_information):
            self.log.info("swing credits were not used on this booking, skipping the history check")
            return
        self.history.open_usage_tab()
        lines = (payment_information or {}).get("players") or {}
        names = self.payment_player_names(players, host) or list(lines)
        rows = [player for player in names if self.history.has_booking_for_player(booking_code, player)]
        if rows:
            for player in rows:
                self.verify_used_credit_by_player(booking_code, player,
                                                  lines.get(player, {}).get("used_credit", ""))
            missing = [player for player in names if player not in rows]
            assert not missing, (
                f"no swing credit row for {amounts.booking_tag(booking_code)} and {missing}")
            return
        total = sum(abs(amounts.to_number(lines.get(player, {}).get("used_credit", "")))
                    for player in names)
        self.verify_used_credit_booking_code(
            booking_code, total or payment_information.get("used_credit", ""))
