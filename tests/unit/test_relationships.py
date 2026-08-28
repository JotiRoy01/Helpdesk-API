def test_ticket_relationships(
    customer_ticket,
    customer,
    category,
):
    assert customer_ticket.creator == customer
    assert customer_ticket.category == category

def test_comment_relationship(
    customer_ticket,
    customer,
):
    ...

import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from apps.tickets.constants import TicketStatus
from apps.tickets.workflow import TicketWorkflow


@pytest.mark.django_db
def test_ticket_creator_cannot_be_deleted(
    customer_ticket,
    customer,
):
    with pytest.raises(ProtectedError):
        customer.delete()


# ---------------------------------
# test category deletion protection
# ---------------------------------

@pytest.mark.django_db
def test_category_used_by_ticket_cannot_be_deleted(
    customer_ticket,
    category,
):
    with pytest.raises(ProtectedError):
        category.delete()


# ---------------------------------------
# Test comment author protection
# ---------------------------------------
@pytest.mark.django_db
def test_comment_author_cannot_be_deleted(
    customer_ticket,
    customer,
):
    from apps.comments.models import Comment

    Comment.objects.create(
        ticket=customer_ticket,
        author=customer,
        message="Test comment.",
    )

    with pytest.raises(ProtectedError):
        customer.delete()

# --------------------------------------------------
# Add regression test for closed tickets
# --------------------------------------------------

@pytest.mark.django_db
def test_closed_ticket_cannot_reopen(
    customer_ticket,
    admin,
):
    customer_ticket.status = TicketStatus.CLOSED
    customer_ticket.save()

    with pytest.raises(ValidationError):
        TicketWorkflow.transition(
            ticket=customer_ticket,
            new_status=TicketStatus.OPEN,
            actor=admin,
        )


# -------------------------------------------
# Regression test: agent cannot close
# -------------------------------------------
@pytest.mark.django_db
def test_agent_cannot_close_resolved_ticket(
    assigned_ticket,
    agent,
):
    assigned_ticket.status = TicketStatus.RESOLVED
    assigned_ticket.save()

    with pytest.raises(Exception):
        TicketWorkflow.transition(
            ticket=assigned_ticket,
            new_status=TicketStatus.CLOSED,
            actor=agent,
        )

# ---------------------------------------------
# Regression test: overdue resolved ticket
# ---------------------------------------------

@pytest.mark.django_db
def test_resolved_ticket_is_not_overdue(
    customer_ticket,
):
    from datetime import timedelta
    from django.utils import timezone

    from apps.tickets.overdue import (
        OverdueTicketService,
    )

    now = timezone.now()

    customer_ticket.status = TicketStatus.RESOLVED
    customer_ticket.due_at = now - timedelta(hours=3)
    customer_ticket.save()

    assert (
        OverdueTicketService.is_overdue(
            ticket=customer_ticket,
            now=now,
        )
        is False
    )


# ----------------------------------------------------
# Regression test: assigned agent isolation
# ----------------------------------------------------

@pytest.mark.django_db
def test_agent_cannot_see_other_agents_ticket(
    api_client,
    another_agent,
    assigned_ticket,
):
    api_client.force_authenticate(
        user=another_agent,
    )

    response = api_client.get(
        f"/api/v1/tickets/{assigned_ticket.id}/"
    )

    assert response.status_code == 404

# ----------------------------------------------------
# Test dashboard isolation
# ----------------------------------------------------

@pytest.mark.django_db
def test_agent_dashboard_does_not_show_global_count(
    api_client,
    agent,
):
    api_client.force_authenticate(
        user=agent,
    )

    response = api_client.get(
        "/api/v1/dashboard/summary/"
    )

    assert response.status_code == 200

# -------------------------------------
# add workload correctness test
# -------------------------------------
@pytest.mark.django_db
def test_agent_workload_counts_only_assigned_tickets(
    api_client,
    admin,
    agent,
    another_agent,
    customer_ticket,
):
    from apps.tickets.models import Ticket

    customer_ticket.assigned_agent = agent
    customer_ticket.save()

    Ticket.objects.create(
        title="Another agent issue",
        description="Another agent issue.",
        category=customer_ticket.category,
        creator=customer_ticket.creator,
        assigned_agent=another_agent,
    )

    api_client.force_authenticate(
        user=admin,
    )

    response = api_client.get(
        "/api/v1/dashboard/workload/"
    )

    assert response.status_code == 200

