from flows.base_flow import BaseFlow
from helpers.checks import CheckTable
from pages.event.event_details_page import EventDetailsPage
from pages.event.registration_method_page import RegistrationMethodPage
from pages.event.select_package_page import SelectPackagePage


class EventPackageFlow(BaseFlow):
    FLOW_NAME = "EventPackageFlow"

    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.details = self.page(EventDetailsPage)
        self.package = self.page(SelectPackagePage)
        self.method = self.page(RegistrationMethodPage)

    # ----------------------------- actions -----------------------------

    def secure_slot(self):
        self.details.tap_secure_slot()
        self.package.verify_screen()

    def find_package(self, name):
        self.package.scroll_to_package(name)

    def set_packages(self, packages):
        self.package.set_packages(packages)

    def confirm_packages(self):
        self.package.tap_confirm_packages()
        self.method.verify_screen()

    def select_packages(self, packages):
        self.set_packages(packages)
        self.confirm_packages()

    def back_to_event_details(self):
        self.package.tap_back()
        self.details.verify_screen()

    def package_names(self, packages):
        return [package["package_name"] if isinstance(package, dict) else str(package)
                for package in packages or []]

    def package_total_players(self, packages):
        return sum(int(package.get("package_qty", 1)) * int(package.get("package_capacity", 1) or 1)
                   for package in packages or [] if isinstance(package, dict))

    # --------------------------- verifications ---------------------------

    def verify_select_package_screen(self, packages):
        table = CheckTable("Select package")
        table.equal("Packages shown", len(self.package_names(packages)), self.package.package_count())
        for package in packages or []:
            name = package["package_name"] if isinstance(package, dict) else str(package)
            self.find_package(name)
            table.contains(f"{name} - package", name, self.package.package_text(name))
            if isinstance(package, dict) and package.get("package_slots"):
                table.contains(f"{name} - slots", package["package_slots"], self.package.package_text(name))
        table.verify()

    def verify_packages_selected(self, packages):
        table = CheckTable("Packages selected")
        for package in packages or []:
            if not isinstance(package, dict):
                continue
            name = package["package_name"]
            self.find_package(name)
            table.equal(f"{name} - quantity", int(package.get("package_qty", 1)),
                        self.package.package_quantity(name))
        table.verify()

    def verify_package_summary(self, packages, total_players="", total_price=""):
        table = CheckTable("Select package summary")
        summary = self.package.player_count_text()
        table.contains("Players", total_players or self.package_total_players(packages), summary)
        if total_price:
            table.amount("Total price", total_price, summary)
        table.truthy("Confirm packages enabled", self.package.confirm_is_enabled())
        table.verify()

    def verify_confirm_packages_disabled(self):
        table = CheckTable("Confirm packages disabled")
        enabled = self.package.confirm_is_enabled()
        expected = "disabled"
        table.add("Confirm packages button", expected, "enabled" if enabled else "disabled", not enabled)
        table.verify()
