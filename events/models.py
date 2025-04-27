from django.contrib.gis.db.models import PointField
from django.db.models import (
    CharField,
    DateTimeField,
    Model,
    SlugField,
    TextChoices,
    URLField,
)
from django.utils.translation import gettext_lazy as _


class Event(Model):

    class EventType(TextChoices):
        HYBRID = "hybrid", _("Hybrid")
        IN_PERSON = "in_person", _("In-Person")
        ONLINE = "online", _("Online")

    name = CharField(_("Event Name"), max_length=255)
    slug = SlugField(unique=True, help_text=_("URL identifier"))
    coordinates = PointField(_("Location"), geography=True)
    datetime = DateTimeField(_("Event Date and Time"))
    time_zone = CharField(_("Time Zone"), max_length=50, blank=True)
    address = CharField(_("Address"), max_length=255)
    description = CharField(
        _("Short Description"),
        blank=True,
        help_text=_("Brief event summary (max 255 characters)"),
        max_length=255,
    )
    event_type = CharField(
        _("Event Format"),
        choices=EventType.choices,
        default=EventType.IN_PERSON,
        help_text=_("Physical, online, or hybrid event type"),
        max_length=12,
    )
    community = CharField(_("Community Name"), max_length=255)
    website = URLField(_("Event Website"), blank=True, null=True)

    class Meta:
        """Model's meta class."""

        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        """Return the model's string representation."""
        return self.name
