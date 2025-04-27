from django.contrib.gis.admin import GISModelAdmin, register

from events.models import Event


@register(Event)
class EventAdmin(GISModelAdmin):
    list_display = (
        "name",
        "coordinates",
        "datetime",
        "event_type",
    )
    list_filter = ["datetime", "event_type"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name", "address", "community"]

    def get_prepopulated_fields(self, request, obj=None):
        """Return prepopulated fields."""
        return {} if obj else self.prepopulated_fields
