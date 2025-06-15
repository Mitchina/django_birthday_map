from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from events.models import Event


class EventFilter(FilterSet):
    """Event filter."""

    date = DateFromToRangeFilter()

    class Meta:
        """Event filter meta."""

        model = Event
        fields = ["date", "event_category"]
