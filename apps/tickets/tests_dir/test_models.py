import pytest

from apps.categories.models import Category
from apps.tickets.constants import TicketPriority, TicketStatus
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_ticket_defaults():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="VPN issue",
        description="Cannot connect to VPN.",
        category=category,
        creator=user,
    )

    assert ticket.status == TicketStatus.OPEN
    assert ticket.priority == TicketPriority.MEDIUM