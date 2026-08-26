from django.urls import path

from .views import (
    TicketDetailView,
    TicketListCreateView,
    TicketTransitionView
)


urlpatterns = [
    path(
        "",
        TicketListCreateView.as_view(),
        name="ticket-list-create",
    ),
    path(
        "<uuid:pk>/",
        TicketDetailView.as_view(),
        name="ticket-detail",
    ),
    path(
        "<uuid:pk>/transition/",
        TicketTransitionView.as_view(),
        name="ticket-transition",
    ),
]