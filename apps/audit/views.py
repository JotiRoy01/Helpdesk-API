from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .permissions import IsAuditAdmin
from .selectors import get_audit_logs
from .serializers import AuditLogSerializer


class AuditLogListView(
    generics.ListAPIView
):
    serializer_class = AuditLogSerializer
    permission_classes = [
        IsAuditAdmin,
    ]

    def get_queryset(self):
        return get_audit_logs()