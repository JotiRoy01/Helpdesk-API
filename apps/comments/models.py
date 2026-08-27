from django.db import models

# Create your models here.
import uuid

from django.conf import settings
from django.db import models

from apps.tickets.models import Ticket


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="comments",
    )

    message = models.TextField(
        max_length=5000,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]

        indexes = [
            models.Index(
                fields=["ticket", "created_at"],
                name="comment_ticket_created_idx",
            ),
            models.Index(
                fields=["author", "created_at"],
                name="comment_author_created_idx",
            ),
        ]

    def __str__(self):
        return f"Comment on {self.ticket_id}"