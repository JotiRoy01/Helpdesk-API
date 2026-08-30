import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from apps.categories.models import Category
from apps.dashboard.selectors import (
    get_agent_workload,
    get_ticket_summary,
)
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_dashboard_summary_uses_small_number_of_queries():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    Ticket.objects.create(
        title="Network issue",
        description="Network issue description.",
        category=category,
        creator=user,
    )

    with CaptureQueriesContext(connection) as queries:
        get_ticket_summary()

    assert len(queries) <= 2


# -----------------------------------------
# Workload query test
# -----------------------------------------
@pytest.mark.django_db
def test_workload_does_not_create_n_plus_one(
    customer,
    category,
):
    agent_one = User.objects.create_user(
        email="agent1@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    agent_two = User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    Ticket.objects.create(
        title="Issue one",
        description="Issue one description.",
        category=category,
        creator=customer,
        assigned_agent=agent_one,
    )

    Ticket.objects.create(
        title="Issue two",
        description="Issue two description.",
        category=category,
        creator=customer,
        assigned_agent=agent_two,
    )

    with CaptureQueriesContext(connection) as queries:
        list(get_agent_workload())

    assert len(queries) <= 2
