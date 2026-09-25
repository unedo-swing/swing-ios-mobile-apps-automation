import pytest

from flows.driving_range_flow import DrivingRangeFlow
from flows.event_flow import EventFlow
from flows.event_package_flow import EventPackageFlow
from flows.group_booking_flow import GroupBookingFlow
from flows.tee_time_flow import TeeTimeFlow
from flows.home_flow import HomeFlow
from flows.login_flow import LoginFlow
from flows.onboarding_flow import OnboardingFlow
from flows.player_details_flow import PlayerDetailsFlow
from flows.swing_credit_flow import SwingCreditFlow
from flows.reschedule_flow import RescheduleFlow
from flows.cancellation_flow import CancellationFlow


@pytest.fixture
def login_flow(driver) -> LoginFlow:
    return LoginFlow(driver)


@pytest.fixture
def home_flow(driver) -> HomeFlow:
    return HomeFlow(driver)


@pytest.fixture
def onboarding_flow(driver) -> OnboardingFlow:
    return OnboardingFlow(driver)


@pytest.fixture
def driving_range_flow(driver) -> DrivingRangeFlow:
    return DrivingRangeFlow(driver)


@pytest.fixture
def swing_credit_flow(driver) -> SwingCreditFlow:
    return SwingCreditFlow(driver)


@pytest.fixture
def tee_time_flow(driver) -> TeeTimeFlow:
    return TeeTimeFlow(driver)


@pytest.fixture
def event_flow(driver) -> EventFlow:
    return EventFlow(driver)


@pytest.fixture
def reschedule_flow(driver) -> RescheduleFlow:
    return RescheduleFlow(driver)


@pytest.fixture
def cancellation_flow(driver) -> CancellationFlow:
    return CancellationFlow(driver)


@pytest.fixture
def player_details_flow(driver) -> PlayerDetailsFlow:
    return PlayerDetailsFlow(driver)


@pytest.fixture
def event_package_flow(driver) -> EventPackageFlow:
    return EventPackageFlow(driver)


@pytest.fixture
def host_group_flow(driver) -> GroupBookingFlow:
    return GroupBookingFlow(driver)
