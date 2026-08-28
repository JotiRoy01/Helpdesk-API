from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema



@extend_schema(
    tags=["System"],
    summary="Application health check",
    description=(
        "Checks whether the application and database "
        "are available."
    ),
)
# class HealthCheckView(APIView):
class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        responses=inline_serializer(
            name="HealthCheckResponse",
            fields={
                "status": serializers.CharField(),
                "services": serializers.DictField(),
            },
        )
    )
    def get(self, request):
        services = {
            "database": "ok",
        }

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            services["database"] = "error"

        healthy = all(
            status == "ok"
            for status in services.values()
        )

        return Response(
            {
                "status": "ok" if healthy else "degraded",
                "services": services,
            },
            status=200 if healthy else 503,
        )