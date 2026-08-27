from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.tickets.selectors import get_visible_tickets_for_user

from .models import Comment


def get_comments_for_ticket(
    *,
    ticket_id,
) -> QuerySet[Comment]:
    return (
        Comment.objects
        .select_related("author")
        .filter(ticket_id=ticket_id)
        .order_by("created_at")
    )


def get_visible_ticket_by_id(
    *,
    ticket_id,
    user,
):
    return get_object_or_404(
        get_visible_tickets_for_user(user=user),
        id=ticket_id,
    )