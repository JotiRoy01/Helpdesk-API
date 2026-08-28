from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .constants import TicketPriority, TicketStatus
from .models import Ticket
from .sla import calculate_due_at
from apps.audit.constants import AuditAction
from apps.audit.services import audit_ticket_action


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
    ip_address=None,
    user_agent="",
):
    created_at = timezone.now()

    due_at = calculate_due_at(
        priority=priority,
        created_at=created_at,
    )

    ticket = Ticket.objects.create(
        title=title.strip(),
        description=description.strip(),
        category=category,
        priority=priority,
        status=TicketStatus.OPEN,
        creator=creator,
        due_at=due_at,
    )

    audit_ticket_action(
        actor=creator,
        action=AuditAction.TICKET_CREATED,
        ticket=ticket,
        new_value={
            "status": TicketStatus.OPEN,
            "priority": priority,
            "category_id": str(category.id),
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return ticket


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
    ip_address=None,
    user_agent="",
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

    previous_agent = ticket.assigned_agent
    ticket.assigned_agent = agent

    ticket.save(
        update_fields=[
            "assigned_agent",
            "updated_at",
        ]
    )

    audit_ticket_action(
        actor=actor,
        action=(
            AuditAction.TICKET_REASSIGNED
            if previous_agent
            else AuditAction.TICKET_ASSIGNED
        ),
        ticket=ticket,
        old_value={
            "assigned_agent": (
                str(previous_agent.id)
                if previous_agent
                else None
            )
        },
        new_value={"assigned_agent": str(agent.id)},
        ip_address=ip_address,
        user_agent=user_agent,
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


