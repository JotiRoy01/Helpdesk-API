import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.categories.models import Category
from apps.tickets.constants import TicketStatus
from apps.tickets.models import Ticket
from apps.tickets.workflow import TicketWorkflow
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Network",
    )


@pytest.fixture
def agent(db):
    return User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )


@pytest.fixture
def customer(db):
    return User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )


@pytest.fixture
def ticket(db, customer, category):
    return Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
    )


@pytest.mark.django_db
def test_open_to_in_progress(ticket, agent):
    updated_ticket = TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.IN_PROGRESS,
        actor=agent,
    )

    assert updated_ticket.status == TicketStatus.IN_PROGRESS



@pytest.mark.django_db
def test_in_progress_to_waiting_for_user(
    ticket,
    agent,
):
    ticket.status = TicketStatus.IN_PROGRESS
    ticket.save()

    updated_ticket = TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.WAITING_FOR_USER,
        actor=agent,
    )

    assert (
        updated_ticket.status
        == TicketStatus.WAITING_FOR_USER
    )


# Test resolution

@pytest.mark.django_db
def test_resolve_ticket(ticket, agent):
    ticket.status = TicketStatus.IN_PROGRESS
    ticket.save()

    updated_ticket = TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.RESOLVED,
        actor=agent,
    )

    assert updated_ticket.status == TicketStatus.RESOLVED
    assert updated_ticket.resolved_at is not None

# Test admin close

@pytest.mark.django_db
def test_admin_can_close_ticket(
    ticket,
    admin,
):
    ticket.status = TicketStatus.RESOLVED
    ticket.save()

    updated_ticket = TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.CLOSED,
        actor=admin,
    )

    assert updated_ticket.status == TicketStatus.CLOSED
    assert updated_ticket.closed_at is not None



# Test agent cannot close
@pytest.mark.django_db
def test_agent_cannot_close_ticket(
    ticket,
    agent,
):
    ticket.status = TicketStatus.RESOLVED
    ticket.save()

    with pytest.raises(ValidationError):
        TicketWorkflow.transition(
            ticket=ticket,
            new_status=TicketStatus.CLOSED,
            actor=agent,
        )


# test customer cannot transition
@pytest.mark.django_db
def test_customer_cannot_change_status(
    ticket,
    customer,
):
    with pytest.raises(ValidationError):
        TicketWorkflow.transition(
            ticket=ticket,
            new_status=TicketStatus.IN_PROGRESS,
            actor=customer,
        )

# test illegal transition
@pytest.mark.django_db
def test_invalid_transition_is_rejected(
    ticket,
    agent,
):
    with pytest.raises(ValidationError):
        TicketWorkflow.transition(
            ticket=ticket,
            new_status=TicketStatus.RESOLVED,
            actor=agent,
        )


# test colsed ticket cannot change

@pytest.mark.django_db
def test_closed_ticket_cannot_transition(
    ticket,
    admin,
):
    ticket.status = TicketStatus.CLOSED
    ticket.save()

    with pytest.raises(ValidationError):
        TicketWorkflow.transition(
            ticket=ticket,
            new_status=TicketStatus.OPEN,
            actor=admin,
        )

# test resolution timestamp
@pytest.mark.django_db
def test_resolution_timestamp_is_set(
    ticket,
    agent,
):
    ticket.status = TicketStatus.IN_PROGRESS
    ticket.save()

    TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.RESOLVED,
        actor=agent,
    )

    ticket.refresh_from_db()

    assert ticket.resolved_at is not None

# test reopen bahavior

@pytest.mark.django_db
def test_resolved_ticket_can_return_to_in_progress(
    ticket,
    agent,
):
    ticket.status = TicketStatus.RESOLVED
    ticket.resolved_at = timezone.now()
    ticket.save()

    original_resolved_at = ticket.resolved_at

    TicketWorkflow.transition(
        ticket=ticket,
        new_status=TicketStatus.IN_PROGRESS,
        actor=agent,
    )

    ticket.refresh_from_db()

    assert ticket.status == TicketStatus.IN_PROGRESS
    assert ticket.resolved_at == original_resolved_at
    assert ticket.closed_at is None

