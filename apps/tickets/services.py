from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .constants import TicketPriority, TicketStatus
from .models import Ticket


SLA_BY_PRIORITY = {
    TicketPriority.LOW: timedelta(hours=72),
    TicketPriority.MEDIUM: timedelta(hours=48),
    TicketPriority.HIGH: timedelta(hours=24),
    TicketPriority.CRITICAL: timedelta(hours=4),
}


def calculate_due_at(*, priority, created_at=None):
    if created_at is None:
        created_at = timezone.now()

    try:
        sla = SLA_BY_PRIORITY[priority]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported priority: {priority}"
        ) from exc

    return created_at + sla


@transaction.atomic
def create_ticket(
    *,
    creator,
    title,
    description,
    category,
    priority,
):
    created_at = timezone.now()

    due_at = calculate_due_at(
        priority=priority,
        created_at=created_at,
    )

    return Ticket.objects.create(
        title=title.strip(),
        description=description.strip(),
        category=category,
        priority=priority,
        status=TicketStatus.OPEN,
        creator=creator,
        due_at=due_at,
    )