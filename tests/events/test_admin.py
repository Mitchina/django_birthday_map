import pytest
from django.contrib.gis.geos import Point

from events.admin import EventAdminForm
from events.models import Event


@pytest.mark.django_db
class TestEventAdminForm:
    def test_event_admin_form_without_coordinates_and_location(self):
        form_data = {
            "name": "Test Event",
            "slug": "test-event",
            "date": "2025-01-01",
            "address": "123 Main St",
            "event_type": "in_person",
            "event_category": "conference",
            "community": "Test Community",
        }
        form = EventAdminForm(data=form_data)
        assert not form.is_valid()
        assert form.errors["location"] == ["No geometry value provided."]

    def test_event_admin_form_location_set_from_coordinates(self):
        form_data = {
            "name": "Test Event",
            "slug": "test-event",
            "location": Point(0.0, 0.0, srid=4326),  # The initial point to the widget
            "latitude": 40.7128,  # The address latitude
            "longitude": -74.0060,  # The address longitude
            "date": "2025-01-01",
            "address": "123 Main St",
            "event_type": "in_person",
            "event_category": "conference",
            "community": "Test Community",
        }
        form = EventAdminForm(data=form_data)
        assert form.is_valid()
        # assert the location was set from the coordinates indicated in the form
        updated_location = form.cleaned_data["location"]
        assert updated_location.x == -74.0060
        assert updated_location.y == 40.7128

        event = form.save(commit=False)
        assert event.location.x == updated_location.x
        assert event.location.y == updated_location.y

    def test_event_admin_form_no_coords_added(self):
        form_data = {
            "name": "Test Event",
            "slug": "test-event",
            "location": Point(0.0, 0.0, srid=4326),  # The widget initial point
            "date": "2025-01-01",
            "address": "123 Main St",
            "event_type": "in_person",
            "event_category": "conference",
            "community": "Test Community",
        }
        form = EventAdminForm(data=form_data)
        assert form.is_valid()
        # The location will keep the initial value
        assert form.cleaned_data["location"].x == 0.0
        assert form.cleaned_data["location"].y == 0.0

    def test_event_admin_form_invalid_coordinates(self):
        form_data = {
            "name": "Invalid coords Event",
            "slug": "invalid-coords-event",
            "latitude": 100.0,  # invalid latitude
            "longitude": 0.0,
            "date": "2025-06-15",
            "address": "123 Main St",
            "event_type": "in_person",
            "event_category": "conference",
            "community": "Test Community",
        }
        form = EventAdminForm(data=form_data)
        assert not form.is_valid()
        assert "Latitude must be between -90 and 90" in str(form.errors)

        form_data["latitude"] = 0.0
        form_data["longitude"] = 200.0  # invalid longitude
        form = EventAdminForm(data=form_data)
        assert not form.is_valid()
        assert "longitude between -180 and 180" in str(form.errors)

    def test_event_admin_form_init_sets_initial_location_for_new_instance(self):
        event = Event()
        form = EventAdminForm(instance=event)

        initial_location = form.fields["location"].initial
        assert isinstance(initial_location, Point)
        assert initial_location.x == 0.0
        assert initial_location.y == 0.0
        assert initial_location.srid == 4326

    def test_event_admin_form_keeps_instance_location(self):
        event = Event.objects.get(slug="pycon-us-2025")
        form_data = {
            "name": event.name,
            "slug": event.slug,
            "location": event.location,
            "latitude": event.latitude,
            "longitude": event.longitude,
            "date": event.date.strftime("%Y-%m-%d"),
            "description": event.description,
            "address": event.address,
            "event_type": event.event_type,
            "event_category": event.event_category,
            "community": event.community,
            "website": event.website,
        }
        form = EventAdminForm(data=form_data, instance=event)
        assert form.is_valid()
        assert not form.has_changed()
        assert form.fields["location"].initial.x == event.location.x
        assert form.fields["location"].initial.y == event.location.y

    def test_event_admin_form_change_instance_location_leaving_coordinates(self):
        """
        Test the EventAdminForm when the instance location point is changed but the coordinates are the same.

        The latitude and longitude coordinates fields win over the location field.
        If the user knows the exact location, they should not add the coordinates.
        """
        event = Event.objects.get(slug="pycon-us-2025")
        assert event.location.x == -79.99471799304133
        assert event.location.y == 40.445853354086616
        form_data = {
            "name": event.name,
            "slug": event.slug,
            "location": Point(-74.0060, 40.7128, srid=4326),
            "latitude": event.latitude,
            "longitude": event.longitude,
            "date": event.date.strftime("%Y-%m-%d"),
            "description": event.description,
            "address": event.address,
            "event_type": event.event_type,
            "event_category": event.event_category,
            "community": event.community,
            "website": event.website,
        }
        form = EventAdminForm(data=form_data, instance=event)
        assert form.is_valid()

        updated_event = form.save(commit=False)
        # The location will not change
        assert updated_event.location.x == -79.99471799304133
        assert updated_event.location.y == 40.445853354086616

    def test_event_admin_form_change_instance_location_removing_coordinates(self):
        """
        Test the EventAdminForm when the instance location point is changed.

        Case the user knows the exact location, they should not add the coordinates.
        """
        event = Event.objects.get(slug="pycon-us-2025")
        assert event.location.x == -79.99471799304133
        assert event.location.y == 40.445853354086616
        form_data = {
            "name": event.name,
            "slug": event.slug,
            "location": Point(-74.0060, 40.7128, srid=4326),
            "date": event.date.strftime("%Y-%m-%d"),
            "description": event.description,
            "address": event.address,
            "event_type": event.event_type,
            "event_category": event.event_category,
            "community": event.community,
            "website": event.website,
        }
        form = EventAdminForm(data=form_data, instance=event)
        assert form.is_valid()

        updated_event = form.save(commit=False)
        # The location will be updated
        assert updated_event.location.x == -74.0060
        assert updated_event.location.y == 40.7128
