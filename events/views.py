from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter

from events.filters import EventFilter
from events.models import Event
from events.serializers import EventSerializer


class EventsMapView(TemplateView):
    """Events map view."""

    template_name = "events/events_map.html"


class EventsAPIViewSet(ReadOnlyModelViewSet):
    """Events API view set."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    bbox_filter_field = "location"
    filter_backends = [InBBoxFilter, DjangoFilterBackend]
    filterset_class = EventFilter
