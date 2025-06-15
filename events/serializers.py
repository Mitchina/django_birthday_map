from rest_framework.serializers import SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from events.models import Event


class EventSerializer(GeoFeatureModelSerializer):
    """Event serializer."""

    event_category_label = SerializerMethodField()

    class Meta:
        """Event serializer meta."""

        fields = [
            "name",
            "slug",
            "date",
            "address",
            "description",
            "event_type",
            "event_category",
            "event_category_label",
            "community",
            "website",
        ]
        geo_field = "location"
        model = Event

    def get_event_category_label(self, obj):
        """Get event category label."""
        return obj.get_event_category_display()
