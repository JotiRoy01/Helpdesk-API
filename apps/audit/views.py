# Create your views here.
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import generics

from .permissions import IsAuditAdmin
from .selectors import get_audit_logs
from .serializers import AuditLogSerializer


@extend_schema(
    tags=["Audit"],
    summary="List audit logs",
    description=(
        "Returns immutable administrative audit records. "
        "Only administrators can access this endpoint."
    ),
    responses=AuditLogSerializer,
)
# class AuditLogListView(
#     generics.ListAPIView
# ):
class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [
        IsAuditAdmin,
    ]

    def get_queryset(self):
        return get_audit_logs()
