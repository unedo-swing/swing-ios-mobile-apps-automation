import pytest

from pages.tee_time.group_booking_intro_page import GroupBookingIntroPage
from pages.tee_time.invite_player_page import InvitePlayerPage
from pages.activity.activity_page import ActivityPage
from pages.app_rating_page import AppRatingPage
from pages.booking_details_page import BookingDetailsPage
from pages.booking_options_page import BookingOptionsPage
from pages.booking_summary_page import BookingSummaryPage
from pages.change_booking_page import ChangeBookingPage
from pages.homepage.coachmark_page import CoachmarkPage
from pages.driving_range.add_promo_code_page import AddPromoCodePage
from pages.driving_range.available_promos_page import AvailablePromosPage
from pages.driving_range.bay_picker_page import BayPickerPage
from pages.driving_range.booking_confirmation_page import BookingConfirmationPage
from pages.driving_range.booking_success_page import BookingSuccessPage
from pages.driving_range.date_picker_page import DatePickerPage
from pages.driving_range.dr_booking_details_page import DrBookingDetailsPage
from pages.driving_range.driving_range_details_page import DrivingRangeDetailsPage
from pages.driving_range.featured_promos_page import FeaturedPromosPage
from pages.driving_range.driving_range_list_page import DrivingRangeListPage
from pages.driving_range.driving_range_search_page import DrivingRangeSearchPage
from pages.driving_range.payment_gateway_page import PaymentGatewayPage
from pages.driving_range.payment_method_page import PaymentMethodPage
from pages.onboarding.birthday_picker_page import BirthdayPickerPage
from pages.event.add_player_page import EventAddPlayerPage
from pages.event.event_details_page import EventDetailsPage
from pages.event.select_package_page import SelectPackagePage
from pages.event.event_list_page import EventListPage
from pages.event.group_registration_info_page import GroupRegistrationInfoPage
from pages.event.player_details_page import PlayerDetailsPage
from pages.event.registration_confirmation_page import RegistrationConfirmationPage
from pages.event.registration_details_page import RegistrationDetailsPage
from pages.event.registration_method_page import RegistrationMethodPage
from pages.event.registration_success_page import RegistrationSuccessPage
from pages.event.registration_summary_page import RegistrationSummaryPage
from pages.tee_time.add_ons_page import AddOnsPage
from pages.tee_time.add_player_page import AddPlayerPage
from pages.tee_time.available_promos_page import TeeTimeAvailablePromosPage
from pages.tee_time.booking_confirmation_page import TeeTimeBookingConfirmationPage
from pages.tee_time.booking_method_page import BookingMethodPage
from pages.tee_time.booking_success_page import TeeTimeBookingSuccessPage
from pages.tee_time.booking_summary_page import TeeTimeBookingSummaryPage
from pages.tee_time.featured_promos_page import TeeTimeFeaturedPromosPage
from pages.tee_time.golf_course_details_page import GolfCourseDetailsPage
from pages.tee_time.group_booking_info_page import GroupBookingInfoPage
from pages.tee_time.tee_time_list_page import TeeTimeListPage
from pages.tee_time.tee_time_search_page import TeeTimeSearchPage
from pages.tee_time.tt_booking_details_page import TeeTimeBookingDetailsPage
from pages.swing_credits.credits_cashbacks_page import CreditsCashbacksPage
from pages.swing_credits.credits_history_page import CreditsHistoryPage
from pages.swing_credits.credits_info_page import CreditsInfoPage
from pages.swing_credits.redeem_credits_page import RedeemCreditsPage
from pages.swing_credits.swing_credits_page import SwingCreditsPage
from pages.onboarding.complete_profile_page import CompleteProfilePage
from pages.onboarding.discovery_source_page import DiscoverySourcePage
from pages.onboarding.gender_picker_page import GenderPickerPage
from pages.onboarding.nationality_picker_page import NationalityPickerPage
from pages.confirm_reschedule_dialog_page import ConfirmRescheduleDialogPage
from pages.confirm_reschedule_page import ConfirmReschedulePage
from pages.add_credit_card_page import AddCreditCardPage
from pages.confirm_credit_card_page import ConfirmCreditCardPage
from pages.purchase_authentication_page import PurchaseAuthenticationPage
from pages.card_linked_success_page import CardLinkedSuccessPage
from pages.country_picker_page import CountryPickerPage
from pages.homepage.home_page import HomePage
from pages.homepage.location_permission_page import LocationPermissionPage
from pages.login_page import LoginPage
from pages.homepage.notification_permission_page import NotificationPermissionPage
from pages.receipt_page import ReceiptPage
from pages.reschedule_booking_page import RescheduleBookingPage
from pages.reschedule_details_page import RescheduleDetailsPage
from pages.reschedule_success_page import RescheduleSuccessPage
from pages.select_date_page import SelectDatePage
from pages.send_receipt_page import SendReceiptPage
from pages.sport_option_page import SportOptionPage
from pages.verification_code_page import VerificationCodePage
from pages.verification_method_page import VerificationMethodPage
from pages.homepage.whats_new_page import WhatsNewPage
from pages.tee_time.credits_earnings_page import TeeTimeCreditsEarningsPage
from pages.cancellation_success_page import CancellationSuccessPage
from pages.cancel_booking_dialog_page import CancelBookingDialogPage


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def country_picker_page(driver) -> CountryPickerPage:
    return CountryPickerPage(driver)


@pytest.fixture
def add_credit_card_page(driver):
    return AddCreditCardPage(driver)


@pytest.fixture
def verification_method_page(driver) -> VerificationMethodPage:
    return VerificationMethodPage(driver)


@pytest.fixture
def verification_code_page(driver) -> VerificationCodePage:
    return VerificationCodePage(driver)


@pytest.fixture
def sport_option_page(driver) -> SportOptionPage:
    return SportOptionPage(driver)


@pytest.fixture
def notification_permission_page(driver) -> NotificationPermissionPage:
    return NotificationPermissionPage(driver)


@pytest.fixture
def location_permission_page(driver) -> LocationPermissionPage:
    return LocationPermissionPage(driver)


@pytest.fixture
def home_page(driver) -> HomePage:
    return HomePage(driver)


@pytest.fixture
def coachmark_page(driver) -> CoachmarkPage:
    return CoachmarkPage(driver)


@pytest.fixture
def whats_new_page(driver) -> WhatsNewPage:
    return WhatsNewPage(driver)


@pytest.fixture
def activity_page(driver) -> ActivityPage:
    return ActivityPage(driver)


@pytest.fixture
def booking_details_page(driver) -> BookingDetailsPage:
    return BookingDetailsPage(driver)


@pytest.fixture
def booking_options_page(driver) -> BookingOptionsPage:
    return BookingOptionsPage(driver)


@pytest.fixture
def booking_summary_page(driver) -> BookingSummaryPage:
    return BookingSummaryPage(driver)


@pytest.fixture
def change_booking_page(driver) -> ChangeBookingPage:
    return ChangeBookingPage(driver)


@pytest.fixture
def reschedule_booking_page(driver) -> RescheduleBookingPage:
    return RescheduleBookingPage(driver)


@pytest.fixture
def select_date_page(driver) -> SelectDatePage:
    return SelectDatePage(driver)


@pytest.fixture
def confirm_reschedule_page(driver) -> ConfirmReschedulePage:
    return ConfirmReschedulePage(driver)


@pytest.fixture
def confirm_reschedule_dialog_page(driver) -> ConfirmRescheduleDialogPage:
    return ConfirmRescheduleDialogPage(driver)


@pytest.fixture
def reschedule_success_page(driver) -> RescheduleSuccessPage:
    return RescheduleSuccessPage(driver)


@pytest.fixture
def reschedule_details_page(driver) -> RescheduleDetailsPage:
    return RescheduleDetailsPage(driver)


@pytest.fixture
def receipt_page(driver) -> ReceiptPage:
    return ReceiptPage(driver)


@pytest.fixture
def send_receipt_page(driver) -> SendReceiptPage:
    return SendReceiptPage(driver)


@pytest.fixture
def app_rating_page(driver) -> AppRatingPage:
    return AppRatingPage(driver)


@pytest.fixture
def complete_profile_page(driver) -> CompleteProfilePage:
    return CompleteProfilePage(driver)


@pytest.fixture
def birthday_picker_page(driver) -> BirthdayPickerPage:
    return BirthdayPickerPage(driver)


@pytest.fixture
def nationality_picker_page(driver) -> NationalityPickerPage:
    return NationalityPickerPage(driver)


@pytest.fixture
def gender_picker_page(driver) -> GenderPickerPage:
    return GenderPickerPage(driver)


@pytest.fixture
def discovery_source_page(driver) -> DiscoverySourcePage:
    return DiscoverySourcePage(driver)


@pytest.fixture
def driving_range_list_page(driver) -> DrivingRangeListPage:
    return DrivingRangeListPage(driver)


@pytest.fixture
def driving_range_search_page(driver) -> DrivingRangeSearchPage:
    return DrivingRangeSearchPage(driver)


@pytest.fixture
def driving_range_details_page(driver) -> DrivingRangeDetailsPage:
    return DrivingRangeDetailsPage(driver)


@pytest.fixture
def date_picker_page(driver) -> DatePickerPage:
    return DatePickerPage(driver)


@pytest.fixture
def bay_picker_page(driver) -> BayPickerPage:
    return BayPickerPage(driver)


@pytest.fixture
def booking_confirmation_page(driver) -> BookingConfirmationPage:
    return BookingConfirmationPage(driver)


@pytest.fixture
def payment_method_page(driver) -> PaymentMethodPage:
    return PaymentMethodPage(driver)


@pytest.fixture
def available_promos_page(driver) -> AvailablePromosPage:
    return AvailablePromosPage(driver)


@pytest.fixture
def add_promo_code_page(driver) -> AddPromoCodePage:
    return AddPromoCodePage(driver)


@pytest.fixture
def payment_gateway_page(driver) -> PaymentGatewayPage:
    return PaymentGatewayPage(driver)


@pytest.fixture
def booking_success_page(driver) -> BookingSuccessPage:
    return BookingSuccessPage(driver)


@pytest.fixture
def dr_booking_details_page(driver) -> DrBookingDetailsPage:
    return DrBookingDetailsPage(driver)


@pytest.fixture
def swing_credits_page(driver) -> SwingCreditsPage:
    return SwingCreditsPage(driver)


@pytest.fixture
def credits_history_page(driver) -> CreditsHistoryPage:
    return CreditsHistoryPage(driver)


@pytest.fixture
def redeem_credits_page(driver) -> RedeemCreditsPage:
    return RedeemCreditsPage(driver)


@pytest.fixture
def credits_info_page(driver) -> CreditsInfoPage:
    return CreditsInfoPage(driver)


@pytest.fixture
def credits_cashbacks_page(driver) -> CreditsCashbacksPage:
    return CreditsCashbacksPage(driver)


@pytest.fixture
def featured_promos_page(driver) -> FeaturedPromosPage:
    return FeaturedPromosPage(driver)


@pytest.fixture
def tee_time_list_page(driver) -> TeeTimeListPage:
    return TeeTimeListPage(driver)


@pytest.fixture
def tee_time_search_page(driver) -> TeeTimeSearchPage:
    return TeeTimeSearchPage(driver)


@pytest.fixture
def golf_course_details_page(driver) -> GolfCourseDetailsPage:
    return GolfCourseDetailsPage(driver)


@pytest.fixture
def tee_time_featured_promos_page(driver) -> TeeTimeFeaturedPromosPage:
    return TeeTimeFeaturedPromosPage(driver)


@pytest.fixture
def booking_method_page(driver) -> BookingMethodPage:
    return BookingMethodPage(driver)


@pytest.fixture
def tee_time_booking_confirmation_page(driver) -> TeeTimeBookingConfirmationPage:
    return TeeTimeBookingConfirmationPage(driver)


@pytest.fixture
def tee_time_available_promos_page(driver) -> TeeTimeAvailablePromosPage:
    return TeeTimeAvailablePromosPage(driver)


@pytest.fixture
def add_ons_page(driver) -> AddOnsPage:
    return AddOnsPage(driver)


@pytest.fixture
def add_player_page(driver) -> AddPlayerPage:
    return AddPlayerPage(driver)


@pytest.fixture
def group_booking_info_page(driver) -> GroupBookingInfoPage:
    return GroupBookingInfoPage(driver)


@pytest.fixture
def tee_time_booking_success_page(driver) -> TeeTimeBookingSuccessPage:
    return TeeTimeBookingSuccessPage(driver)


@pytest.fixture
def tee_time_booking_details_page(driver) -> TeeTimeBookingDetailsPage:
    return TeeTimeBookingDetailsPage(driver)


@pytest.fixture
def tee_time_booking_summary_page(driver) -> TeeTimeBookingSummaryPage:
    return TeeTimeBookingSummaryPage(driver)


@pytest.fixture
def event_list_page(driver) -> EventListPage:
    return EventListPage(driver)


@pytest.fixture
def event_details_page(driver) -> EventDetailsPage:
    return EventDetailsPage(driver)


@pytest.fixture
def select_package_page(driver):
    return SelectPackagePage(driver)


@pytest.fixture
def registration_method_page(driver) -> RegistrationMethodPage:
    return RegistrationMethodPage(driver)


@pytest.fixture
def registration_confirmation_page(driver) -> RegistrationConfirmationPage:
    return RegistrationConfirmationPage(driver)


@pytest.fixture
def player_details_page(driver) -> PlayerDetailsPage:
    return PlayerDetailsPage(driver)


@pytest.fixture
def event_add_player_page(driver) -> EventAddPlayerPage:
    return EventAddPlayerPage(driver)


@pytest.fixture
def group_registration_info_page(driver) -> GroupRegistrationInfoPage:
    return GroupRegistrationInfoPage(driver)


@pytest.fixture
def registration_success_page(driver) -> RegistrationSuccessPage:
    return RegistrationSuccessPage(driver)


@pytest.fixture
def registration_details_page(driver) -> RegistrationDetailsPage:
    return RegistrationDetailsPage(driver)


@pytest.fixture
def registration_summary_page(driver) -> RegistrationSummaryPage:
    return RegistrationSummaryPage(driver)


@pytest.fixture
def tee_time_credits_earnings_page(driver) -> TeeTimeCreditsEarningsPage:
    return TeeTimeCreditsEarningsPage(driver)


@pytest.fixture
def cancel_booking_dialog_page(driver) -> CancelBookingDialogPage:
    return CancelBookingDialogPage(driver)


@pytest.fixture
def cancellation_success_page(driver) -> CancellationSuccessPage:
    return CancellationSuccessPage(driver)


@pytest.fixture
def purchase_authentication_page(driver) -> PurchaseAuthenticationPage:
    return PurchaseAuthenticationPage(driver)


@pytest.fixture
def card_linked_success_page(driver) -> CardLinkedSuccessPage:
    return CardLinkedSuccessPage(driver)


@pytest.fixture
def confirm_credit_card_page(driver) -> ConfirmCreditCardPage:
    return ConfirmCreditCardPage(driver)


@pytest.fixture
def group_booking_intro_page(driver) -> GroupBookingIntroPage:
    return GroupBookingIntroPage(driver)


@pytest.fixture
def invite_player_page(driver) -> InvitePlayerPage:
    return InvitePlayerPage(driver)
