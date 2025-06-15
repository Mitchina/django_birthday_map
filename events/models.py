from django.contrib.gis.db.models import PointField
from django.db.models import (
    CharField,
    DateField,
    FloatField,
    Model,
    SlugField,
    TextChoices,
    URLField,
)
from django.utils.translation import gettext_lazy as _


class Event(Model):
    """Event model."""

    class EventType(TextChoices):
        """Event type."""

        HYBRID = "hybrid", _("Hybrid")
        IN_PERSON = "in_person", _("On-Site")
        ONLINE = "online", _("Online")

    class EventCategory(TextChoices):
        """Event category."""

        LOCAL_COMMUNITY = "local_community", _("Local Community")
        CONFERENCE = "conference", _("Conference")

    name = CharField(_("Event Name"), max_length=255)
    slug = SlugField(unique=True, help_text=_("URL identifier"))
    location = PointField(_("Location"), geography=True)
    latitude = FloatField(null=True, blank=True)
    longitude = FloatField(null=True, blank=True)
    date = DateField(_("Event Date"))
    address = CharField(_("Address"), max_length=255)
    description = CharField(
        _("Short Description"),
        blank=True,
        help_text=_(
            "Provide a brief summary of the event, including the full event dates "
            "(e.g., May 14 - May 22, 2025), as well as the time and time zone if relevant. "
            "Maximum 255 characters."
        ),
        max_length=255,
    )
    event_type = CharField(
        _("Event Format"),
        choices=EventType.choices,
        default=EventType.IN_PERSON,
        help_text=_("Specify if on-site, online or hybrid event type"),
        max_length=12,
    )
    event_category = CharField(
        max_length=20,
        choices=EventCategory.choices,
        default=EventCategory.LOCAL_COMMUNITY,
        help_text=_("Classify the event as a local community event or a conference"),
    )
    community = CharField(_("Community Name"), max_length=255)
    website = URLField(_("Event Post or Website"), blank=True, null=True)

    class Meta:
        """Model's meta class."""

        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        """Return the model's string representation."""
        return self.name
