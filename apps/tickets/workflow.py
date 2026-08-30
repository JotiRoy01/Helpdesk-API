from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.audit.constants import AuditAction
from apps.audit.services import audit_ticket_action
from apps.users.constants import UserRole

from .constants import (
    ALLOWED_TRANSITIONS,
    TicketStatus,
)


class TicketWorkflow:
    """
    Encapsulates ticket state transition rules.

    Views should never directly mutate ticket.status.
    """

    @staticmethod
    def validate_transition(
        *,
        current_status,
        new_status,
    ):
        if current_status == new_status:
            raise ValidationError("Ticket is already in this status.")

        allowed_statuses = ALLOWED_TRANSITIONS.get(
            current_status,
            set(),
        )

        if new_status not in allowed_statuses:
            raise ValidationError(
                f"Cannot transition ticket from {current_status} to {new_status}."
            )

    @staticmethod
    def validate_actor(
        *,
        actor,
        current_status,
        new_status,
    ):
        if actor.role == UserRole.ADMIN:
            return

        if actor.role != UserRole.SUPPORT_AGENT:
            raise ValidationError(
                "Only support agents or admins can change ticket status."
            )

        if new_status == TicketStatus.CLOSED:
            raise ValidationError("Only admins can close tickets.")

    @staticmethod
    def validate_assignment(*, actor, ticket):
        """Ensure an agent can only update their assigned tickets."""
        if actor.role == UserRole.ADMIN:
            return

        if actor.role != UserRole.SUPPORT_AGENT:
            raise ValidationError(
                "Only support agents or admins can update ticket assignments."
            )

        if (
            ticket.assigned_agent_id is not None
            and ticket.assigned_agent_id != actor.id
        ):
            raise ValidationError(
                "Support agents can only update tickets assigned to them."
            )

    @classmethod
    @transaction.atomic
    def transition(cls, *, ticket, new_status, actor, ip_address=None, user_agent=""):
        previous_status = ticket.status

        cls.validate_assignment(
            actor=actor,
            ticket=ticket,
        )

        cls.validate_transition(
            current_status=ticket.status,
            new_status=new_status,
        )

        cls.validate_actor(
            actor=actor,
            current_status=ticket.status,
            new_status=new_status,
        )

        now = timezone.now()

        ticket.status = new_status

        if new_status == TicketStatus.RESOLVED:
            ticket.resolved_at = now

        elif new_status == TicketStatus.CLOSED:
            ticket.closed_at = now

        elif new_status == TicketStatus.IN_PROGRESS:
            ticket.closed_at = None

        ticket.save(
            update_fields=[
                "status",
                "resolved_at",
                "closed_at",
                "updated_at",
            ]
        )

        audit_ticket_action(
            actor=actor,
            action=AuditAction.TICKET_STATUS_CHANGED,
            ticket=ticket,
            old_value={"status": previous_status},
            new_value={"status": new_status},
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return ticket


# -------------------------------
# -------------------------------

from rest_framework import serializers

from apps.users.models import User


class TicketAssignmentSerializer(serializers.Serializer):
    assigned_agent = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(
            role=UserRole.SUPPORT_AGENT,
            is_active=True,
        ),
        allow_null=False,
    )
