from django.urls import path

from .views import (
    DashboardSummaryView,
    DashboardWorkloadView,
)

urlpatterns = [
    path(
        "summary/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary",
    ),
    path(
        "workload/",
        DashboardWorkloadView.as_view(),
        name="dashboard-workload",
    ),
]
