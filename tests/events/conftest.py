import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from events.models import Event


@pytest.fixture
def api_client():
    """The API client."""
    return APIClient()


@pytest.fixture(scope="session", autouse=True)
def events(django_db_setup, django_db_blocker):
    """
    Load the 'events' fixture once per test session.

    The fixture data will be available for all tests and cleaned up after the session.
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "events", database="default")


@pytest.fixture
def conferences_in_may_2025(db):
    """Conferences in May 2025."""
    return Event.objects.filter(
        date__year=2025, date__month=5, event_category="conference"
    )
