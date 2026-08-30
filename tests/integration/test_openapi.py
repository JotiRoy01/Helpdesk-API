from django.urls import reverse
from rest_framework.test import APIClient


def test_openapi_schema_is_available():
    client = APIClient()

    response = client.get(reverse("schema"))

    assert response.status_code == 200


def test_swagger_ui_is_available():
    client = APIClient()

    response = client.get(reverse("swagger-ui"))

    assert response.status_code == 200


def test_redoc_is_available():
    client = APIClient()

    response = client.get(reverse("redoc"))

    assert response.status_code == 200
