from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        database_status = "ok"

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            database_status = "error"

        status_code = 200 if database_status == "ok" else 503

        return Response(
            {
                "status": "ok" if status_code == 200 else "degraded",
                "services": {
                    "database": database_status,
                },
            },
            status=status_code,
        )