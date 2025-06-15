from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventsAPIViewSet, EventsMapView

app_name = "events"

api_router = DefaultRouter()
api_router.register(r"", EventsAPIViewSet, basename="events-api")


urlpatterns = [
    # Frontend
    path("", EventsMapView.as_view(), name="events-map"),
    # API
    path("api/", include(api_router.urls)),
]
