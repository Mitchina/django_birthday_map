from rest_framework_gis.serializers import GeoFeatureModelSerializer

from events.models import Event


class EventSerializer(GeoFeatureModelSerializer):
    class Meta:
        fields = [
            "name",
            "slug",
            "datetime",
            "time_zone",
            "address",
            "description",
            "event_type",
            "community",
            "website",
        ]
        geo_field = "coordinates"
        model = Event
