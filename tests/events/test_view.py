from django.urls import reverse


def test_events_map_view(client):
    """Test the events map view."""
    response = client.get(reverse("events:events-map"))
    assert response.status_code == 200
