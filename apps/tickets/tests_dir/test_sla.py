from datetime import timedelta

import pytest
from django.utils import timezone

from apps.tickets.constants import TicketPriority
from apps.tickets.sla import (
    SLA_POLICIES,
    calculate_due_at,
)


@pytest.mark.parametrize(
    "priority,hours",
    [
        (TicketPriority.LOW, 72),
        (TicketPriority.MEDIUM, 48),
        (TicketPriority.HIGH, 24),
        (TicketPriority.CRITICAL, 4),
    ],
)
def test_sla_policy(
    priority,
    hours,
):
    assert SLA_POLICIES[priority].duration == timedelta(hours=hours)


def test_calculate_due_at():
    created_at = timezone.now()

    due_at = calculate_due_at(
        priority=TicketPriority.CRITICAL,
        created_at=created_at,
    )

    assert due_at == created_at + timedelta(hours=4)


# -------------------------------------
# test overdue detection
# -------------------------------------

from apps.tickets.constants import (
    TicketPriority,
    TicketStatus,
)
from apps.tickets.models import Ticket
from apps.tickets.overdue import (
    OverdueTicketService,
)


@pytest.mark.django_db
def test_ticket_is_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.OPEN
    ticket.due_at = now - timedelta(minutes=1)
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is True
    )


# ---------------------------------------
# test future ticket is not overdue
# ---------------------------------------
@pytest.mark.django_db
def test_future_ticket_is_not_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.OPEN
    ticket.due_at = now + timedelta(hours=1)
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is False
    )


# --------------------------------------
# test resolved ticket is not overdue
# --------------------------------------
@pytest.mark.django_db
def test_resolved_ticket_is_not_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.RESOLVED
    ticket.due_at = now - timedelta(hours=10)
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is False
    )


# ---------------------------------------
# test closed ticket
# ---------------------------------------
@pytest.mark.django_db
def test_closed_ticket_is_not_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.CLOSED
    ticket.due_at = now - timedelta(hours=10)
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is False
    )


# ---------------------------------------
# test null deadline
# ---------------------------------------
@pytest.mark.django_db
def test_ticket_without_due_date_is_not_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.OPEN
    ticket.due_at = None
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is False
    )


@pytest.mark.django_db
def test_ticket_due_exactly_now_is_not_overdue(
    ticket,
):
    now = timezone.now()

    ticket.status = TicketStatus.OPEN
    ticket.due_at = now
    ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=ticket,
            now=now,
        )
        is False
    )


from apps.tickets.overdue import (
    overdue_ticket_queryset,
)


# ---------------------------------
# test bulk overdue query
# ---------------------------------
@pytest.mark.django_db
def test_overdue_queryset_returns_only_overdue_tickets(
    customer,
    category,
):
    now = timezone.now()

    Ticket.objects.create(
        title="Overdue ticket",
        description="This ticket is overdue.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
        due_at=now - timedelta(hours=1),
    )

    Ticket.objects.create(
        title="Future ticket",
        description="This ticket is not overdue.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
        due_at=now + timedelta(hours=1),
    )

    Ticket.objects.create(
        title="Resolved ticket",
        description="This ticket is resolved.",
        category=category,
        creator=customer,
        status=TicketStatus.RESOLVED,
        due_at=now - timedelta(hours=1),
    )

    overdue = overdue_ticket_queryset()

    assert overdue.count() == 1
    assert overdue.first().title == "Overdue ticket"


# -------------------------------------
# test overdue count
# -------------------------------------
from apps.tickets.overdue import (
    count_overdue_tickets,
)


@pytest.mark.django_db
def test_count_overdue_tickets(
    customer,
    category,
):
    now = timezone.now()

    Ticket.objects.create(
        title="Overdue one",
        description="First overdue ticket.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
        due_at=now - timedelta(hours=1),
    )

    Ticket.objects.create(
        title="Overdue two",
        description="Second overdue ticket.",
        category=category,
        creator=customer,
        status=TicketStatus.IN_PROGRESS,
        due_at=now - timedelta(hours=2),
    )

    assert count_overdue_tickets() == 2
