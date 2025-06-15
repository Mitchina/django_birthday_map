from django.contrib.gis.admin import GISModelAdmin, register
from django.contrib.gis.forms import OSMWidget
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from events.models import Event


class EventAdminForm(ModelForm):
    """
    Event admin form.

    # Info for developers/admin users on adding location from the admin:

    - If you know the longitude and latitude of the event address but don't know the exact point to place the marker on
      the map, you can input the latitude and longitude fields directly. The form will automatically convert these
      coordinates into a Point, and the marker will be placed accordingly on the map.

    - To get longitude and latitude, you can use Google Maps:
      Right-click on the desired location and copy the coordinates.
      Coordinates are copied in this order: longitude, latitude

    - Note: The latitude and longitude fields take precedence over the Point selected on the map.
      If you know the exact location on the map, you can simply choose it without filling in the latitude and longitude
      fields.
    """

    class Meta:
        """Event admin form meta."""

        model = Event
        fields = [
            "name",
            "slug",
            "location",
            "latitude",
            "longitude",
            "date",
            "description",
            "address",
            "event_type",
            "event_category",
            "community",
            "website",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize form."""
        super().__init__(*args, **kwargs)
        if not self.instance.pk or not self.instance.location:
            self.fields["location"].initial = Point(0.0, 0.0, srid=4326)

    def clean(self):
        """Clean form."""
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitude")
        lon = cleaned_data.get("longitude")
        if lat is not None and lon is not None:
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValidationError(
                    "Latitude must be between -90 and 90 and longitude between -180 and 180."
                )
            self.fields["location"].widget = OSMWidget(
                attrs={
                    "default_lat": lat,
                    "default_lon": lon,
                }
            )
            point = Point(lon, lat)
            cleaned_data["location"] = point
            self.fields["location"].initial = point
        return cleaned_data

    def save(self, commit=True):
        """Save form."""
        self.instance.location = self.cleaned_data["location"]
        return super().save(commit=commit)


@register(Event)
class EventAdmin(GISModelAdmin):
    """Event admin."""

    form = EventAdminForm
    list_display = (
        "name",
        "location",
        "date",
        "event_type",
        "event_category",
    )
    list_filter = ["date", "event_type", "event_category", "community"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name", "address", "community"]

    def get_prepopulated_fields(self, request, obj=None):
        """Return prepopulated fields."""
        return {} if obj else self.prepopulated_fields

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Formfield for dbfield."""
        if db_field.name == "location":
            kwargs["widget"] = self.gis_widget(**self.gis_widget_kwargs)
            kwargs["widget"].map_srid = 4326
        return super().formfield_for_dbfield(db_field, request, **kwargs)
