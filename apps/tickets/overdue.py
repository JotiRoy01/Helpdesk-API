from django.utils import timezone

from .constants import TicketStatus
from .models import Ticket

ACTIVE_STATUSES = {
    TicketStatus.OPEN,
    TicketStatus.IN_PROGRESS,
    TicketStatus.WAITING_FOR_USER,
}


def is_ticket_overdue(
    *,
    ticket,
    now=None,
):
    now = now or timezone.now()

    if ticket.status not in ACTIVE_STATUSES:
        return False

    if ticket.due_at is None:
        return False

    return ticket.due_at < now


# ---------------------------------------------------
# create and efficient queryset for overdue tickets
# ---------------------------------------------------
def overdue_ticket_queryset():
    now = timezone.now()

    return Ticket.objects.filter(
        due_at__lt=now,
        status__in=ACTIVE_STATUSES,
    ).select_related(
        "category",
        "creator",
        "assigned_agent",
    )


# ------------------------------
# add count helper
# ------------------------------
def count_overdue_tickets():
    return overdue_ticket_queryset().count()


# --------------------------------
# add assigned-agent overdue query
# ---------------------------------
def overdue_tickets_for_agent(*, agent):
    return overdue_ticket_queryset().filter(
        assigned_agent=agent,
    )


# ----------------------------------
# better: expose a queryset helper
# ----------------------------------
def filter_overdue(
    queryset,
    *,
    now=None,
):
    now = now or timezone.now()

    return queryset.filter(
        due_at__lt=now,
        status__in=ACTIVE_STATUSES,
    )


def filter_not_overdue(
    queryset,
    *,
    now=None,
):
    now = now or timezone.now()

    from django.db.models import Q

    return queryset.filter(
        ~Q(
            due_at__lt=now,
            status__in=ACTIVE_STATUSES,
        )
    )


# ------------------------------------------
# add an overdue processing operation
# ------------------------------------------
class OverdueTicketService:
    @staticmethod
    def is_overdue(
        *,
        ticket,
        now=None,
    ):
        return is_ticket_overdue(
            ticket=ticket,
            now=now,
        )

    @staticmethod
    def get_overdue_tickets():
        return overdue_ticket_queryset()

    @staticmethod
    def count():
        return count_overdue_tickets()
