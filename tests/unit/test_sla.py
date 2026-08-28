from datetime import timedelta

import pytest
from django.utils import timezone

from apps.tickets.constants import TicketPriority
from apps.tickets.sla import (
    SLA_POLICIES,
    calculate_due_at,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("priority", "hours"),
    [
        (TicketPriority.LOW, 72),
        (TicketPriority.MEDIUM, 48),
        (TicketPriority.HIGH, 24),
        (TicketPriority.CRITICAL, 4),
    ],
)
def test_sla_policy(priority, hours):
    assert (
        SLA_POLICIES[priority].duration
        == timedelta(hours=hours)
    )


def test_calculate_due_at():
    created_at = timezone.now()

    result = calculate_due_at(
        priority=TicketPriority.CRITICAL,
        created_at=created_at,
    )

    assert result == (
        created_at + timedelta(hours=4)
    )

# -----------------------------------
# Test SLA invalid priority
# -----------------------------------
def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError):
        calculate_due_at(
            priority="INVALID",
        )