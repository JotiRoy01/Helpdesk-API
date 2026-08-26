from django.db import models

# Create your models here.
import uuid

from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from apps.categories.models import Category

from .constants import TicketPriority, TicketStatus


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
        ],
    )

    description = models.TextField(
        validators=[
            MinLengthValidator(10),
        ],
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    priority = models.CharField(
        max_length=10,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
        db_index=True,
    )

    status = models.CharField(
        max_length=25,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
        db_index=True,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tickets",
    )

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "tickets"
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["status", "created_at"],
                name="ticket_status_created_idx",
            ),
            models.Index(
                fields=["priority", "created_at"],
                name="ticket_priority_created_idx",
            ),
            models.Index(
                fields=["assigned_agent", "status"],
                name="ticket_agent_status_idx",
            ),
            models.Index(
                fields=["creator", "created_at"],
                name="ticket_creator_created_idx",
            ),
            models.Index(
                fields=["category", "status"],
                name="ticket_category_status_idx",
            ),
            models.Index(
                fields=["due_at", "status"],
                name="ticket_due_status_idx",
            ),
        ]

    def __str__(self):
        return self.title