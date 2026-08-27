import pytest
from unittest.mock import Mock
from apps.categories.models import Category
from apps.tickets.constants import TicketPriority, TicketStatus
from apps.tickets.filters import TicketFilter
from apps.tickets.models import Ticket
from apps.tickets.selectors import get_visible_tickets_for_user
from apps.tickets.views import TicketListCreateView
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_filter_by_status():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    Ticket.objects.create(
        title="Open ticket",
        description="Open ticket description.",
        category=category,
        creator=user,
        status=TicketStatus.OPEN,
    )

    Ticket.objects.create(
        title="Resolved ticket",
        description="Resolved ticket description.",
        category=category,
        creator=user,
        status=TicketStatus.RESOLVED,
    )

    queryset = Ticket.objects.filter(
        creator=user,
    )

    filtered = TicketFilter(
        {
            "status": TicketStatus.OPEN,
        },
        queryset=queryset,
    ).qs

    assert filtered.count() == 1
    assert filtered.first().status == TicketStatus.OPEN

# -------------------------
# Test priority filtering
# -------------------------
@pytest.mark.django_db
def test_filter_by_priority():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    Ticket.objects.create(
        title="Critical issue",
        description="Critical issue description.",
        category=category,
        creator=user,
        priority=TicketPriority.CRITICAL,
    )

    Ticket.objects.create(
        title="Low issue",
        description="Low issue description.",
        category=category,
        creator=user,
        priority=TicketPriority.LOW,
    )

    queryset = Ticket.objects.filter(
        creator=user,
    )

    filtered = TicketFilter(
        {
            "priority": TicketPriority.CRITICAL,
        },
        queryset=queryset,
    ).qs

    assert filtered.count() == 1
    assert (
        filtered.first().priority
        == TicketPriority.CRITICAL
    )

# -----------------------------
# Test category filtering
# -----------------------------
@pytest.mark.django_db
def test_filter_by_category():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    network = Category.objects.create(
        name="Network",
    )

    hardware = Category.objects.create(
        name="Hardware",
    )

    Ticket.objects.create(
        title="Router issue",
        description="Network router issue.",
        category=network,
        creator=user,
    )

    Ticket.objects.create(
        title="Laptop issue",
        description="Laptop hardware issue.",
        category=hardware,
        creator=user,
    )

    queryset = Ticket.objects.filter(
        creator=user,
    )

    filtered = TicketFilter(
        {
            "category": str(network.id),
        },
        queryset=queryset,
    ).qs

    assert filtered.count() == 1
    assert filtered.first().category == network

# ---------------------------------
# Test assigned-agent filtering
# ---------------------------------
@pytest.mark.django_db
def test_filter_by_assigned_agent():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    category = Category.objects.create(
        name="Network",
    )

    Ticket.objects.create(
        title="Agent ticket",
        description="Assigned ticket.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    queryset = Ticket.objects.all()

    filtered = TicketFilter(
        {
            "assigned_agent": str(agent.id),
        },
        queryset=queryset,
    ).qs

    assert filtered.count() == 1

# ----------------------------------
# Test pagination limit
# ----------------------------------

from apps.common.pagination import (
    StandardResultsSetPagination,
)


def test_default_page_size():
    pagination = StandardResultsSetPagination()

    assert pagination.page_size == 20


def test_max_page_size():
    pagination = StandardResultsSetPagination()

    assert pagination.max_page_size == 100

# ----------------------------------------
# Test visibility + filtering together
# ----------------------------------------
@pytest.mark.django_db
def test_customer_filter_cannot_escape_ownership(
    customer,
    another_customer,
    category,
):
    Ticket.objects.create(
        title="My open ticket",
        description="My ticket.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
    )

    Ticket.objects.create(
        title="Other open ticket",
        description="Other ticket.",
        category=category,
        creator=another_customer,
        status=TicketStatus.OPEN,
    )

    queryset = get_visible_tickets_for_user(
        user=customer,
    )

    filtered = TicketFilter(
        {
            "status": TicketStatus.OPEN,
        },
        queryset=queryset,
    ).qs

    assert filtered.count() == 1
    assert filtered.first().creator == customer

# -------------------------
# Test search
# -------------------------
@pytest.mark.django_db
def test_ticket_search():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    Ticket.objects.create(
        title="VPN connection issue",
        description="Cannot connect to office VPN.",
        category=category,
        creator=user,
    )

    Ticket.objects.create(
        title="Printer issue",
        description="Printer is offline.",
        category=category,
        creator=user,
    )

    queryset = get_visible_tickets_for_user(
        user=user,
    )

    from rest_framework.filters import SearchFilter

    backend = SearchFilter()

    request = Mock()
    request.query_params = {
        "search": "VPN",
    }

    filtered = backend.filter_queryset(
        request,
        queryset,
        TicketListCreateView,
    )

    assert filtered.count() == 1

