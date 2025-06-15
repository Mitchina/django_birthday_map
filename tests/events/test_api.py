from django.urls import reverse

from events.serializers import EventSerializer


def test_events_api_view(api_client, conferences_in_may_2025):
    """Test the events API view."""
    query_params = {
        "date_after": "2025-05-01",
        "date_before": "2025-05-31",
        "event_category": "conference",
    }
    response = api_client.get(reverse("events:events-api-list"), query_params)
    assert response.status_code == 200
    serializer = EventSerializer(conferences_in_may_2025, many=True)
    assert response.json() == serializer.data
    assert len(response.json()["features"]) == conferences_in_may_2025.count()
    assert response.json()["features"][0]["properties"]["name"] == "PyCon US 2025"
    assert response.json()["features"][0]["properties"]["date"] == "2025-05-14"
