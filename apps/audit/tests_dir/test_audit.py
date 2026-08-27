import pytest

from apps.audit.constants import AuditAction
from apps.audit.models import AuditLog
from apps.categories.models import Category
from apps.tickets.constants import TicketPriority
from apps.tickets.constants import TicketStatus
from apps.tickets.services import create_ticket
from apps.tickets.services import assign_ticket
from apps.tickets.workflow import TicketWorkflow
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_ticket_creation_creates_audit():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = create_ticket(
        creator=customer,
        title="VPN problem",
        description="VPN connection fails.",
        category=category,
        priority=TicketPriority.HIGH,
    )

    audit = AuditLog.objects.get(
        entity_id=ticket.id,
    )

    assert audit.action == AuditAction.TICKET_CREATED
    assert audit.actor == customer



@pytest.mark.django_db
def test_assignment_creates_audit(
    admin,
    agent,
    ticket,
):
    assign_ticket(
        ticket=ticket,
        agent=agent,
        actor=admin,
    )

    audit = AuditLog.objects.filter(
        entity_id=ticket.id,
        action=AuditAction.TICKET_ASSIGNED,
    ).first()

    assert audit is not None
    assert audit.new_value["assigned_agent"] == str(
        agent.id
    )


# ----------------------------
# test reassignment audit
# ----------------------------
@pytest.mark.django_db
def test_reassignment_creates_correct_audit(
    admin,
    agent,
    ticket,
):
    second_agent = User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    assign_ticket(
        ticket=ticket,
        agent=agent,
        actor=admin,
    )

    assign_ticket(
        ticket=ticket,
        agent=second_agent,
        actor=admin,
    )

    audit = AuditLog.objects.filter(
        entity_id=ticket.id,
        action=AuditAction.TICKET_REASSIGNED,
    ).latest("created_at")

    assert audit.old_value["assigned_agent"] == str(agent.id)
    assert audit.new_value["assigned_agent"] == str(second_agent.id)

# ---------------------------------------
# Test workflow audit
# ---------------------------------------
@pytest.mark.django_db
def test_status_transition_creates_audit(
    admin,
    ticket,
):
    TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.CLOSED,
        actor=admin,
    )


