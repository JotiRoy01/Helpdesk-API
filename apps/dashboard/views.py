from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import CanViewDashboard, IsAdminDashboard
from .serializers import (
    AgentWorkloadSerializer,
    DashboardSummarySerializer,
)
from .services import (
    get_dashboard_summary,
    get_dashboard_workload,
)


class DashboardSummaryView(APIView):
    permission_classes = [
        CanViewDashboard,
    ]

    def get(self, request):
        summary = get_dashboard_summary()

        serializer = DashboardSummarySerializer(
            summary,
        )

        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ------------------------------------
# Create workload view
# ------------------------------------
class DashboardWorkloadView(APIView):
    permission_classes = [
        #CanViewDashboard,
        IsAdminDashboard
    ]

    def get(self, request):
        workload = get_dashboard_workload()

        serializer = AgentWorkloadSerializer(
            workload,
            many=True,
        )

        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
