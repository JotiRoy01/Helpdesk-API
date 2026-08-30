from django.db import transaction

from .models import AuditLog

# from apps.audit.services import audit_ticket_action


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
