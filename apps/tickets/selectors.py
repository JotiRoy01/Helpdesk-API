from django.db.models import QuerySet

from apps.users.constants import UserRole

from .models import Ticket
from .exceptions import TicketNotFoundError


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


def get_visible_tickets_for_user(
    *,
    user,
) -> QuerySet[Ticket]:
    queryset = ticket_queryset()

    if user.role == UserRole.ADMIN:
        return queryset

    if user.role == UserRole.SUPPORT_AGENT:
        return queryset.filter(
            assigned_agent=user,
        )

    if user.role == UserRole.CUSTOMER:
        return queryset.filter(
            creator=user,
        )

    return queryset.none()


def get_ticket_by_id(ticket_id):
    try:
        return ticket_queryset().get(
            id=ticket_id,
        )
    except Ticket.DoesNotExist as exc:
        raise TicketNotFoundError() from exc


def get_ticket_for_update(ticket_id):
    try:
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
    except Ticket.DoesNotExist as exc:
        raise TicketNotFoundError() from exc


# ------------------------------------------
# In step 9
# ------------------------------------------
def get_ticket_for_update_for_user(
    *,
    ticket_id,
    user,
):
    queryset = (
        Ticket.objects
        .select_for_update()
        .select_related(
            "category",
            "creator",
            "assigned_agent",
        )
    )

    if user.role == UserRole.ADMIN:
        return queryset.get(id=ticket_id)

    if user.role == UserRole.SUPPORT_AGENT:
        return queryset.get(
            id=ticket_id,
            assigned_agent=user,
        )

    if user.role == UserRole.CUSTOMER:
        return queryset.get(
            id=ticket_id,
            creator=user,
        )

    return queryset.none().get(id=ticket_id)

# ---------------------------
# ---------------------------
from django.db.models import QuerySet

from apps.users.constants import UserRole

from .models import Ticket


def get_ticket_for_assignment(
    *,
    ticket_id,
):
    return (
        Ticket.objects
        .select_for_update()
        .select_related(
            "category",
            "creator",
            "assigned_agent",
        )
        .get(
            id=ticket_id,
        )
    )


from .exceptions import TicketNotFoundError


def get_visible_ticket_by_id(
    *,
    ticket_id,
    user,
):
    try:
        return get_visible_tickets_for_user(
            user=user,
        ).get(
            id=ticket_id,
        )
    except Ticket.DoesNotExist as exc:
        raise TicketNotFoundError() from exc