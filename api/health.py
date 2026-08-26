from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

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