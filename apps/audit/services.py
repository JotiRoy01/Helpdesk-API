from django.db import transaction

from .models import AuditLog
from apps.audit.constants import AuditAction
#from apps.audit.services import audit_ticket_action


@transaction.atomic
def create_audit_log(
    *,
    actor,
    action,
    entity_type,
    entity_id,
    old_value=None,
    new_value=None,
    metadata=None,
    ip_address=None,
    user_agent="",
):
    return AuditLog.objects.create(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_value=old_value,
        new_value=new_value,
        metadata=metadata or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )

# ---------------------------------
# add a clear convenience function
# ---------------------------------
def audit_ticket_action(
    *,
    actor,
    action,
    ticket,
    old_value=None,
    new_value=None,
    metadata=None,
    ip_address=None,
    user_agent="",
):
    return create_audit_log(
        actor=actor,
        action=action,
        entity_type="Ticket",
        entity_id=ticket.id,
        old_value=old_value,
        new_value=new_value,
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
    )


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

# ----------------------------------------
# pass request metadata from the view
# ----------------------------------------
# def perform_create(self, serializer):
#     data = serializer.validated_data

#     ticket = create_ticket(
#         creator=self.request.user,
#         title=data["title"],
#         description=data["description"],
#         category=data["category"],
#         priority=data["priority"],
#         ip_address=self.request.META.get(
#             "REMOTE_ADDR"
#         ),
#         user_agent=self.request.META.get(
#             "HTTP_USER_AGENT",
#             "",
#         ),
#     )

#     serializer.instance = ticket

# -----------------------------------
# Audit Assignment
# -----------------------------------
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

    action = (
        AuditAction.TICKET_REASSIGNED
        if previous_agent
        else AuditAction.TICKET_ASSIGNED
    )

    audit_ticket_action(
        actor=actor,
        action=action,
        ticket=ticket,
        old_value={
            "assigned_agent": (
                str(previous_agent.id)
                if previous_agent
                else None
            )
        },
        new_value={
            "assigned_agent": str(agent.id),
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return ticket

# ----------------------------------
# Audit priority changes
# ----------------------------------
@transaction.atomic
def update_ticket_priority(
    *,
    ticket,
    priority,
    actor,
    ip_address=None,
    user_agent="",
):
    previous_priority = ticket.priority

    if previous_priority == priority:
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

    audit_ticket_action(
        actor=actor,
        action=AuditAction.TICKET_PRIORITY_CHANGED,
        ticket=ticket,
        old_value={
            "priority": previous_priority,
        },
        new_value={
            "priority": priority,
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return ticket

