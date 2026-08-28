from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .permissions import CanViewDashboard, IsAdminDashboard
from .serializers import (
    AgentWorkloadSerializer,
    DashboardSummarySerializer,
)
from .services import (
    get_dashboard_summary,
    get_dashboard_workload,
)


@extend_schema(
    tags=["Dashboard"],
    summary="Get dashboard summary",
    description=(
        "Administrators receive global ticket statistics. "
        "Support agents receive statistics for tickets "
        "assigned to them. Customers are denied access."
    ),
    responses=DashboardSummarySerializer,
)
# class DashboardSummaryView(APIView):
class DashboardSummaryView(APIView):
    permission_classes = [
        CanViewDashboard,
    ]

    @extend_schema(responses={200: DashboardSummarySerializer})
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

@extend_schema(
    tags=["Dashboard"],
    summary="Get support-agent workload",
    description=(
        "Returns team-wide workload statistics. "
        "Only administrators can access this endpoint."
    ),
    responses=AgentWorkloadSerializer(many=True),
)
# class DashboardWorkloadView(APIView):
class DashboardWorkloadView(APIView):
    permission_classes = [
        #CanViewDashboard,
        IsAdminDashboard
    ]

    @extend_schema(responses={200: AgentWorkloadSerializer(many=True)})
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
