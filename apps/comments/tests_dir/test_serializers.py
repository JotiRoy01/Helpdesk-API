import pytest

from apps.categories.models import Category
from apps.comments.services import create_comment
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


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

from apps.comments.serializers import (
    CommentCreateSerializer,
)


def test_comment_rejects_empty_message():
    serializer = CommentCreateSerializer(
        data={
            "message": "   ",
        }
    )

    assert serializer.is_valid() is False
    assert "message" in serializer.errors