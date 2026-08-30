import pytest

from apps.categories.models import Category
from apps.comments.services import create_comment
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_create_comment():
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
        description="VPN connection is failing.",
        category=category,
        creator=user,
    )

    comment = create_comment(
        ticket=ticket,
        author=user,
        message="I have additional information.",
    )

    assert comment.ticket == ticket
    assert comment.author == user
    assert comment.message == "I have additional information."


# -----------------------------------
# Test message trimming
# -----------------------------------
@pytest.mark.django_db
def test_comment_message_is_trimmed():
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
        description="VPN connection is failing.",
        category=category,
        creator=user,
    )

    comment = create_comment(
        ticket=ticket,
        author=user,
        message="   Hello support.   ",
    )

    assert comment.message == "Hello support."
