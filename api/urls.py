from django.urls import include, path

from .health import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path(
        "categories/",
        include("apps.categories.urls"),
    ),
    path("tickets/", include("apps.tickets.urls")),
    path(
        "auth/",
        include("apps.users.urls"),
    ),
    path(
        "",
        include("apps.comments.urls"),
    ),
    path(
        "dashboard/",
        include("apps.dashboard.urls"),
    ),
    path(
        "audit-logs/",
        include("apps.audit.urls"),
    ),
]
