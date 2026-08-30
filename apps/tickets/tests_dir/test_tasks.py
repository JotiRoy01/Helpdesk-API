from datetime import timedelta

import pytest

# pyrefly: ignore [missing-import]
from django.utils import timezone

from apps.tickets.constants import TicketStatus
from apps.tickets.models import Ticket
from apps.tickets.tasks import process_overdue_tickets


@pytest.mark.django_db
def test_process_overdue_tickets():
    result = process_overdue_tickets()

    assert isinstance(result, int)


# -----------------------------------
# test SLA task with overdue ticket
# -----------------------------------


@pytest.mark.django_db
def test_overdue_task_counts_overdue_tickets(
    customer,
    category,
):
    Ticket.objects.create(
        title="Overdue task test",
        description="This ticket should be overdue.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
        due_at=timezone.now() - timedelta(hours=1),
    )

    assert process_overdue_tickets() == 1
