from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .constants import TicketPriority, TicketStatus
from .models import Ticket
from .sla import calculate_due_at


SLA_BY_PRIORITY = {
    TicketPriority.LOW: timedelta(hours=72),
    TicketPriority.MEDIUM: timedelta(hours=48),
    TicketPriority.HIGH: timedelta(hours=24),
    TicketPriority.CRITICAL: timedelta(hours=4),
}


# def calculate_due_at(*, priority, created_at=None):
#     if created_at is None:
#         created_at = timezone.now()

#     try:
#         sla = SLA_BY_PRIORITY[priority]
#     except KeyError as exc:
#         raise ValueError(
#             f"Unsupported priority: {priority}"
#         ) from exc

#     return created_at + sla


# @transaction.atomic
# def create_ticket(
#     *,
#     creator,
#     title,
#     description,
#     category,
#     priority,
# ):
#     created_at = timezone.now()

#     due_at = calculate_due_at(
#         priority=priority,
#         created_at=created_at,
#     )

#     return Ticket.objects.create(
#         title=title.strip(),
#         description=description.strip(),
#         category=category,
#         priority=priority,
#         status=TicketStatus.OPEN,
#         creator=creator,
#         due_at=due_at,
#     )

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


# --------------------------
# --------------------------
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.users.constants import UserRole

from .models import Ticket


@transaction.atomic
def assign_ticket(
    *,
    ticket,
    agent,
    actor,
):
    if actor.role != UserRole.ADMIN:
        raise ValidationError(
            "Only administrators can assign tickets."
        )

    if agent.role != UserRole.SUPPORT_AGENT:
        raise ValidationError(
            "Tickets can only be assigned to support agents."
        )

    if not agent.is_active:
        raise ValidationError(
            "Cannot assign a ticket to an inactive agent."
        )

    ticket.assigned_agent = agent

    ticket.save(
        update_fields=[
            "assigned_agent",
            "updated_at",
        ]
    )

    return ticket

# -------------------------------
# Create priority update service
# -------------------------------
@transaction.atomic
def update_ticket_priority(
    *,
    ticket,
    priority,
):
    if ticket.priority == priority:
        return ticket

    ticket.priority = priority

    ticket.due_at = calculate_due_at(
        priority=priority,
        created_at=ticket.created_at,
    )

    ticket.save(
        update_fields=[
            "priority",
            "due_at",
            "updated_at",
        ]
    )

    return ticket


