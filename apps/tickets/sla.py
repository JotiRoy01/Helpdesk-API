from dataclasses import dataclass
from datetime import timedelta

from django.utils import timezone

from .constants import TicketPriority, TicketStatus
from .models import Ticket


@dataclass(frozen=True)
class SLAPolicy:
    duration: timedelta


SLA_POLICIES = {
    TicketPriority.LOW: SLAPolicy(
        duration=timedelta(hours=72),
    ),
    TicketPriority.MEDIUM: SLAPolicy(
        duration=timedelta(hours=48),
    ),
    TicketPriority.HIGH: SLAPolicy(
        duration=timedelta(hours=24),
    ),
    TicketPriority.CRITICAL: SLAPolicy(
        duration=timedelta(hours=4),
    ),
}

# ------------------------------
# calculate due time
# ------------------------------
def calculate_due_at(
    *,
    priority,
    created_at=None,
):
    created_at = created_at or timezone.now()

    try:
        policy = SLA_POLICIES[priority]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported ticket priority: {priority}"
        ) from exc

    return created_at + policy.duration


