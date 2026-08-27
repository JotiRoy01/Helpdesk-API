from django.urls import path

from .health import HealthCheckView
from django.urls import include, path


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path(
        "categories/",
        include("apps.categories.urls"),
    ),
    path(
        "tickets/",
        include("apps.tickets.urls")
    ),
    path(
        "auth/",
        include("apps.users.urls"),
    ),
    path(
        "",
        include("apps.comments.urls"),
    ),
]