import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_is_throttled():
    client = APIClient()

    payload = {
        "email": "missing@example.com",
        "password": "WrongPassword123!",
    }

    responses = []

    for _ in range(6):
        responses.append(
            client.post(
                "/api/v1/auth/login/",
                payload,
                format="json",
            )
        )

    assert any(response.status_code == 429 for response in responses)
