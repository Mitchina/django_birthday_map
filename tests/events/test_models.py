from events.models import Event


def test_event_str():
    """Test the Event string representation."""
    assert str(Event(name="Django 20th birthday 2025")) == "Django 20th birthday 2025"
