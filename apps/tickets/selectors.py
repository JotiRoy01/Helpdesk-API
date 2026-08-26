from django.db.models import QuerySet

from .models import Ticket


def ticket_queryset() -> QuerySet[Ticket]:
    return (
        Ticket.objects
        .select_related(
            "category",
            "creator",
            "assigned_agent",
        )
        .all()
    )


def get_ticket_by_id(ticket_id):
    return ticket_queryset().get(
        id=ticket_id,
    )


from django.db import transaction


def get_ticket_for_update(ticket_id):
    return (
        Ticket.objects
        .select_for_update()
        .select_related(
            "category",
            "creator",
            "assigned_agent",
        )
        .get(id=ticket_id)
    )