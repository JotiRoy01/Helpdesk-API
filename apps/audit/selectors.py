from .models import AuditLog


def get_audit_logs():
    return (
        AuditLog.objects
        .select_related("actor")
        .all()
        .order_by("-created_at")
    )