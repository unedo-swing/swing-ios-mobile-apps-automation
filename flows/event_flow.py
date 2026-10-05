from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from pages.homepage.home_page import HomePage
from pages.event.event_list_page import EventListPage
from pages.event.event_details_page import EventDetailsPage
from pages.event.registration_method_page import RegistrationMethodPage
from pages.event.registration_confirmation_page import RegistrationConfirmationPage
from pages.event.player_details_page import PlayerDetailsPage
from pages.event.add_player_page import EventAddPlayerPage
from pages.country_picker_page import CountryPickerPage
from pages.event.group_registration_info_page import GroupRegistrationInfoPage
from pages.payment_method_page import PaymentMethodPage
from pages.payment_gateway_page import PaymentGatewayPage
from pages.event.registration_success_page import RegistrationSuccessPage
from pages.event.registration_details_page import RegistrationDetailsPage
from pages.event.registration_summary_page import RegistrationSummaryPage
from pages.tee_time.available_promos_page import TeeTimeAvailablePromosPage
from pages.event.select_package_page import SelectPackagePage
from helpers import amounts


class EventFlow(BaseFlow):
    FLOW_NAME = "EventFlow"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.list = self.page(EventListPage)
        self.details = self.page(EventDetailsPage)
        self.method = self.page(RegistrationMethodPage)
        self.confirm = self.page(RegistrationConfirmationPage)
        self.promos = self.page(TeeTimeAvailablePromosPage)
        self.player_form = self.page(PlayerDetailsPage)
        self.player = self.page(EventAddPlayerPage)
        self.country = self.page(CountryPickerPage)
        self.group_info = self.page(GroupRegistrationInfoPage)
        self.payment = self.page(PaymentMethodPage)
        self.gateway = self.page(PaymentGatewayPage)
        self.success = self.page(RegistrationSuccessPage)
        self.registration = self.page(RegistrationDetailsPage)
        self.summary = self.page(RegistrationSummaryPage)
        self.package = self.page(SelectPackagePage)

    # ----------------------------- actions -----------------------------

    def open_events(self):
        self.home.open_events()
        self.list.verify_screen()

    def only_swing_pass_partners(self):
        self.list.scroll_to_swing_pass_filter()
        self.list.enable_swing_pass_filter()
        self.list.verify_screen()

    def all_partners(self):
        self.list.scroll_to_swing_pass_filter()
        self.list.disable_swing_pass_filter()
        self.list.verify_screen()

    def find_event(self, text):
        self.list.scroll_to_card(text)

    def open_event(self, text):
        self.list.open_card(text)
        self.details.verify_screen()

    def see_event_information(self):
        self.details.scroll_to_registration_fee()

    def secure_slot(self):
        self.details.tap_secure_slot()
        self.method.verify_screen()

    def select_package(self, packages):
        self.package.set_packages(packages)
        self.package.tap_confirm_packages()

    def choose_standard_registration(self):
        self.method.choose_standard_registration()
        self.confirm.verify_screen()

    def choose_group_registration(self):
        self.method.choose_group_registration()
        self.confirm.verify_screen()

    def open_registration_method(self):
        self.confirm.open_registration_method()
        self.method.verify_screen()

    def switch_to_group_registration(self):
        self.group_info.switch_to_group_registration()
        self.confirm.verify_screen()

    def close_group_registration_info(self):
        self.group_info.tap_close()
        self.confirm.verify_screen()

    def open_player_details(self, player):
        self.confirm.open_player_details(player)
        self.player_form.verify_screen()

    def answer_question(self, option):
        self.player_form.select_option(option)

    def find_question(self, text):
        self.player_form.scroll_to_question(text)

    def download_hcp_template(self):
        self.player_form.download_template()

    def upload_hcp_file(self):
        self.player_form.upload_file()

    def save_player_details(self):
        self.player_form.tap_save()
        self.confirm.verify_screen()

    def use_swing_credits(self):
        self.confirm.toggle_swing_credits()

    def enter_note(self, text):
        self.confirm.enter_note(text)

    def add_player(self):
        self.confirm.add_player()
        self.player.verify_screen()

    def search_friend(self, name):
        self.player.search_friend(name)

    def select_friend(self, username):
        self.player.select_friend(username)
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
        self.confirm.verify_screen()

    def remove_player(self, player):
        self.confirm.remove_player(player)

    def select_flight(self, name):
        self.confirm.select_flight(name)

    def let_organizer_arrange_flight(self):
        self.confirm.toggle_organizer_arrange()

    def open_payment_method(self):
        self.confirm.change_payment_method()
        self.payment.verify_screen()

    def choose_payment_method(self, name):
        self.open_payment_method()
        self.payment.select_method(name)
        self.confirm.verify_screen()
    
    def add_player_each_packages(self, player):
        self.confirm.remove_player_without_name()
        

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

    def invite_players(self, players):
        for player in players or []:
            if str(player.get("add_method", "")).lower() not in ("", "host"):
                self.invite_player(player)

    def fill_players_details(self, player, answer=""):
        self.open_player_details(player["player"])
        if answer:
            self.answer_question(answer)
        self.save_player_details()

    def open_promos(self, player):
        self.confirm.open_promos(player)
        self.promos.verify_screen()

    def apply_player_promo(self, player, promo_name):
        self.open_promos(player)
        self.promos.search_promo(promo_name)
        self.promos.apply_promo()
        self.confirm.verify_screen()

    def apply_player_promos(self, players):
        for player in players or []:
            if player.get("promo_name"):
                self.apply_player_promo(player["player"], player["promo_name"])

    def get_payment_information_before_payment(self, used_credit="0"):
        payment_info = {"total_payment": self.confirm.total_payment_text(),
                        "earned_credit": self.confirm.earned_credits_text()}
        if str(used_credit) == "1":
            payment_info["used_credit"] = self.confirm.used_credits_text()
        return payment_info

    def get_registration_code_after_payment(self):
        return self.success.registration_code_text()

    def pay_now(self):
        self.confirm.tap_pay_now()

    def proceed_to_pay(self):
        self.gateway.verify_screen()
        self.gateway.tap_proceed_to_pay()

    def finish(self):
        self.success.tap_finish()

    def open_registration_details(self):
        self.success.open_registration_details()
        self.registration.verify_screen()

    def open_complete_breakdown(self):
        self.registration.open_breakdown()
        self.summary.verify_screen()

    def back_to_registration_details(self):
        self.summary.tap_back()
        self.registration.verify_screen()

    # --------------------------- verifications ---------------------------

    def verify_select_page(self):
        self.package.verify_screen()

    def verify_registration_confirmation(self):
        self.confirm.verify_screen()

    def verify_registration_confirmation_players(self, players):
        self.confirm.verify_screen()
        assert self.confirm.player_count() == self.player_total(players), (
            f"expected {self.player_total(players)} players, found {self.confirm.player_count()}")
        for player in self.player_names(players):
            assert self.confirm.has_player(player), f"{player} not in the registration"

    def verify_registration_information(self, date, starting_time, venue, registration_type, players):
        self.confirm.verify_screen()
        assert date in self.confirm.date_text(), (
            f"date does not match: expected {date}, found {self.confirm.date_text()}")
        assert starting_time in self.confirm.starting_time_text(), (
            f"starting time does not match: expected {starting_time}, "
            f"found {self.confirm.starting_time_text()}")
        assert venue in self.confirm.venue_text(), (
            f"venue does not match: expected {venue}, found {self.confirm.venue_text()}")
        if registration_type:
            assert registration_type in self.confirm.registration_type_text(), (
                f"registration type does not match: expected {registration_type}, "
                f"found {self.confirm.registration_type_text()}")
        assert str(self.player_total(players)) in self.confirm.players_text(), (
            f"player count does not match: expected {self.player_total(players)}, "
            f"found {self.confirm.players_text()}")

    def verify_players_promos(self, players):
        names = [player["promo_name"] for player in players or [] if player.get("promo_name")]
        for player in players or []:
            text = self.confirm.player_promo_text(player["player"])
            if player.get("promo_name"):
                assert player["promo_name"] in text, (
                    f"{player['player']} does not show the promo: expected "
                    f"{player['promo_name']}, found {text}")
            else:
                for name in names:
                    assert name not in text, f"{player['player']} should not use the promo {name}"

    def package_names(self, packages):
        return [package["package_name"] if isinstance(package, dict) else str(package)
                for package in packages or []]

    def package_capacity(self, package):
        return int(package.get("package_capacity", 1) or 1)

    def package_players(self, packages):
        return sum(int(package.get("package_qty", 0)) * self.package_capacity(package)
                   for package in packages or [] if isinstance(package, dict))

    def verify_multi_price_packages(self, packages, players=None):
        table = CheckTable("Registration packages")
        table.equal("Packages shown", len(self.package_names(packages)), self.confirm.package_count())
        for package in packages or []:
            name = package["package_name"] if isinstance(package, dict) else str(package)
            self.confirm.scroll_to_package(name)
            table.contains(f"{name} - package", name, self.confirm.package_text(name))
            if isinstance(package, dict) and package.get("package_slots"):
                table.contains(f"{name} - slots", package["package_slots"], self.confirm.package_text(name))
            if isinstance(package, dict) and package.get("package_players") is not None:
                table.equal(f"{name} - players assigned", package["package_players"],
                            self.confirm.package_player_count(name))
        table.verify()

    def verify_multi_price_players(self, packages, players=None):
        table = CheckTable("Players per package")
        for package in packages or []:
            name = package["package_name"] if isinstance(package, dict) else str(package)
            self.confirm.scroll_to_package(name)
            assigned = self.confirm.package_player_items(name)
            for player in self.player_names(package.get("players") if isinstance(package, dict) else None):
                table.add(f"{name} - {player}", "in the package",
                          "in the package" if any(player in text for text in assigned) else "not found",
                          any(player in text for text in assigned))
            if isinstance(package, dict) and package.get("package_full") is not None:
                full = not self.confirm.has_add_player_in_package(name)
                table.add(f"{name} - slots filled", bool(package["package_full"]), full,
                          full == bool(package["package_full"]))
        table.verify()

    def verify_multi_price_registration(self, event_name, date, starting_time, venue, players,
                                        packages=(), total_price="", registration_type="Standard registration"):
        self.confirm.verify_screen()
        table = CheckTable("Registration confirmation")
        table.contains("Event name", event_name, self.confirm.event_title_text(event_name))
        table.contains("Date", date, self.confirm.date_text())
        table.contains("Starting time", starting_time, self.confirm.starting_time_text())
        table.contains("Venue", venue, self.confirm.venue_text())
        table.contains("Player", self.player_total(players), self.confirm.players_text())
        if registration_type:
            table.contains("Registration type", registration_type, self.confirm.registration_type_text())
        if total_price:
            table.amount("Total price", total_price, self.confirm.total_price_text())
        table.verify()
        self.verify_multi_price_packages(packages, players)

    def verify_registration_success(self):
        self.success.verify_screen()

    def verify_payment_success_event(self, date, starting_time, payment_information, players,
                                     venue="", payment_method=""):
        self.success.verify_screen()
        assert self.success.registration_code_text(), "registration code not shown"
        assert date in self.success.date_text(), (
            f"date does not match: expected {date}, found {self.success.date_text()}")
        assert starting_time in self.success.starting_time_text(), (
            f"starting time does not match: expected {starting_time}, "
            f"found {self.success.starting_time_text()}")
        assert str(self.player_total(players)) in self.success.players_text(), ( # type: ignore
            f"player count does not match: expected {self.player_total(players)}, "
            f"found {self.success.players_text()}")
        assert amounts.to_number(payment_information["total_payment"]) == amounts.to_number(
            self.success.total_text()), (
            f"total does not match: expected {payment_information['total_payment']}, "
            f"found {self.success.total_text()}")
        if venue:
            assert venue in self.success.venue_text(), ( # type: ignore
                f"venue does not match: expected {venue}, found {self.success.venue_text()}")
        if payment_method:
            assert payment_method in self.success.payment_method_text(), ( # type: ignore
                f"payment method does not match: expected {payment_method}, "
                f"found {self.success.payment_method_text()}")

    def verify_registration_details(self, registration_code, date, starting_time, venue="",
                                    status="UPCOMING"):
        self.registration.verify_screen()
        assert registration_code in self.registration.registration_code_text(), (
            f"registration code does not match: expected {registration_code}, "
            f"found {self.registration.registration_code_text()}")
        assert date in self.registration.date_text(), (
            f"date does not match: expected {date}, found {self.registration.date_text()}")
        assert starting_time in self.registration.starting_time_text(), (
            f"starting time does not match: expected {starting_time}, "
            f"found {self.registration.starting_time_text()}")
        if venue:
            assert venue in self.registration.venue_text(), ( # type: ignore
                f"venue does not match: expected {venue}, found {self.registration.venue_text()}")
        if status:
            assert self.registration.has_status(status), (
                f"registration status {status} not shown")
