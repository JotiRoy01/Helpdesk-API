from datetime import timedelta

import pytest
from django.utils import timezone

from apps.categories.models import Category
from apps.tickets.constants import TicketPriority, TicketStatus
from apps.tickets.services import (
    calculate_due_at,
    create_ticket,
    update_ticket_priority,
)
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def customer(db):
    return User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Network",
    )


@pytest.mark.django_db
def test_calculate_high_priority_sla():
    created_at = timezone.now()

    due_at = calculate_due_at(
        priority=TicketPriority.HIGH,
        created_at=created_at,
    )

    assert due_at == created_at + timedelta(hours=24)


@pytest.mark.django_db
def test_create_ticket(customer, category):
    ticket = create_ticket(
        creator=customer,
        title="VPN issue",
        description="The VPN cannot connect.",
        category=category,
        priority=TicketPriority.CRITICAL,
    )

    assert ticket.creator == customer
    assert ticket.category == category
    assert ticket.status == TicketStatus.OPEN
    assert ticket.priority == TicketPriority.CRITICAL
    assert ticket.due_at is not None


# -------------------------------------
# Test priority update recalculates SLA
# -------------------------------------
@pytest.mark.django_db
def test_priority_update_recalculates_due_at(
    ticket,
):
    original_due_at = ticket.due_at

    update_ticket_priority(
        ticket=ticket,
        priority=TicketPriority.CRITICAL,
    )

    ticket.refresh_from_db()

    assert ticket.priority == TicketPriority.CRITICAL
    assert ticket.due_at != original_due_at
    assert ticket.due_at == (ticket.created_at + timedelta(hours=4))
