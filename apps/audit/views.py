from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .permissions import IsAuditAdmin
from .selectors import get_audit_logs
from .serializers import AuditLogSerializer
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)


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
class AuditLogListView(
    generics.ListAPIView
):
    serializer_class = AuditLogSerializer
    permission_classes = [
        IsAuditAdmin,
    ]

    def get_queryset(self):
        return get_audit_logs()