import pytest

from rest_framework.test import APIClient

from apps.users.constants import UserRole
from apps.users.models import User
from apps.tickets.constants import TicketStatus
from apps.tickets.models import Ticket
from apps.dashboard.selectors import (
    get_agent_summary,
    get_ticket_summary,
)


@pytest.mark.django_db
def test_customer_cannot_access_dashboard():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    client = APIClient()

    client.force_authenticate(
        user=customer,
    )

    response = client.get(
        "/api/v1/dashboard/summary/"
    )

    assert response.status_code == 403

# -----------------------------------------
# test agent summary
# -----------------------------------------
@pytest.mark.django_db
def test_agent_can_access_own_summary():
    agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    client = APIClient()

    client.force_authenticate(
        user=agent,
    )

    response = client.get(
        "/api/v1/dashboard/summary/"
    )

    assert response.status_code == 200


# ---------------------------------------
# Test agent cannot see workload
# ---------------------------------------
@pytest.mark.django_db
def test_agent_cannot_access_team_workload():
    agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    client = APIClient()

    client.force_authenticate(
        user=agent,
    )

    response = client.get(
        "/api/v1/dashboard/workload/"
    )

    assert response.status_code == 403

# ----------------------------------------
# test admin access
# ----------------------------------------
@pytest.mark.django_db
def test_admin_can_access_workload():
    admin = User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )

    client = APIClient()

    client.force_authenticate(
        user=admin,
    )

    response = client.get(
        "/api/v1/dashboard/workload/"
    )

    assert response.status_code == 200

# ------------------------------------------
# test actual summary counts
# ------------------------------------------
@pytest.mark.django_db
def test_admin_summary_counts(
    admin,
    customer,
    category,
):
    Ticket.objects.create(
        title="Open issue",
        description="Open ticket description.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
    )

    Ticket.objects.create(
        title="Resolved issue",
        description="Resolved ticket description.",
        category=category,
        creator=customer,
        status=TicketStatus.RESOLVED,
    )

    Ticket.objects.create(
        title="Closed issue",
        description="Closed ticket description.",
        category=category,
        creator=customer,
        status=TicketStatus.CLOSED,
    )

    summary = get_ticket_summary()

    assert summary["total"] == 3
    assert summary["open"] == 1
    assert summary["resolved"] == 1
    assert summary["closed"] == 1


# ----------------------------------------
# Test agent-specific summary
# ----------------------------------------
@pytest.mark.django_db
def test_agent_summary_is_scoped_to_agent(
    agent,
    another_agent,
    customer,
    category,
):
    Ticket.objects.create(
        title="Agent one ticket",
        description="Agent one ticket.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    Ticket.objects.create(
        title="Agent two ticket",
        description="Agent two ticket.",
        category=category,
        creator=customer,
        assigned_agent=another_agent,
    )

    summary = get_agent_summary(
        agent=agent,
    )

    assert summary["total"] == 1

