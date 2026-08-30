from django.contrib import admin

# Register your models here.
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "entity_type",
        "entity_id",
        "actor",
        "created_at",
    )

    list_filter = (
        "action",
        "entity_type",
    )

    search_fields = (
        "actor__email",
        "entity_id",
    )

    readonly_fields = (
        "id",
        "actor",
        "action",
        "entity_type",
        "entity_id",
        "old_value",
        "new_value",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
    )

    ordering = ("-created_at",)
