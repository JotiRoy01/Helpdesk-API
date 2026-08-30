# Create your models here.
import uuid

from django.conf import settings
from django.db import models

from .constants import AuditAction


class AuditLog(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=40,
        choices=AuditAction.choices,
        db_index=True,
    )

    entity_type = models.CharField(
        max_length=50,
        db_index=True,
    )

    entity_id = models.UUIDField(
        db_index=True,
    )

    old_value = models.JSONField(
        null=True,
        blank=True,
    )

    new_value = models.JSONField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    "entity_type",
                    "entity_id",
                    "created_at",
                ],
                name="audit_entity_created_idx",
            ),
            models.Index(
                fields=[
                    "actor",
                    "created_at",
                ],
                name="audit_actor_created_idx",
            ),
            models.Index(
                fields=[
                    "action",
                    "created_at",
                ],
                name="audit_action_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.action} - {self.entity_type}:{self.entity_id}"
