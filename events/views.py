from django.views.generic import TemplateView
from rest_framework.viewsets import ReadOnlyModelViewSet

from events.models import Event
from events.serializers import EventSerializer

# from rest_framework_gis.filters import InBBoxFilter


class EventsMapView(TemplateView):
    template_name = "events_map.html"


class EventsViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    bbox_filter_field = "coordinates"
