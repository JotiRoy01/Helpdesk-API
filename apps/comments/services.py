from django.db import transaction

from .models import Comment


@transaction.atomic
def create_comment(
    *,
    ticket,
    author,
    message,
):
    return Comment.objects.create(
        ticket=ticket,
        author=author,
        message=message.strip(),
    )