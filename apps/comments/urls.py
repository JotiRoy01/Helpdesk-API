from django.urls import path

from .views import TicketCommentListCreateView


urlpatterns = [
    path(
        "tickets/<uuid:ticket_id>/comments/",
        TicketCommentListCreateView.as_view(),
        name="ticket-comments",
    ),
]