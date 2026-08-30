from unittest.mock import Mock

from apps.common.exception_handler import (
    custom_exception_handler,
)
from apps.common.exceptions import (
    ResourceNotFoundError,
)


def test_application_error_format():
    request = Mock()
    request.request_id = "test-request-id"

    context = {
        "request": request,
    }

    response = custom_exception_handler(
        ResourceNotFoundError(
            message="Resource not found.",
            code="RESOURCE_NOT_FOUND",
        ),
        context,
    )

    assert response.status_code == 404
    assert response.data["success"] is False
    assert response.data["code"] == "RESOURCE_NOT_FOUND"
    assert response.data["request_id"] == "test-request-id"


from rest_framework.exceptions import ValidationError


def test_validation_error_format():
    request = Mock()
    request.request_id = "test-request-id"

    context = {
        "request": request,
    }

    response = custom_exception_handler(
        ValidationError({"email": ["Invalid email."]}),
        context,
    )

    assert response.status_code == 400
    assert response.data["success"] is False
    assert response.data["code"] == "VALIDATION_ERROR"
    assert "email" in response.data["errors"]


from rest_framework.exceptions import PermissionDenied


def test_permission_error_format():
    request = Mock()
    request.request_id = "test-request-id"

    context = {
        "request": request,
    }

    response = custom_exception_handler(
        PermissionDenied(),
        context,
    )

    assert response.status_code == 403
    assert response.data["success"] is False
    assert response.data["code"] == "FORBIDDEN"


def test_unexpected_exception_does_not_leak_details():
    request = Mock()
    request.request_id = "test-request-id"

    context = {
        "request": request,
    }

    secret_value = "super-secret-database-password"

    response = custom_exception_handler(
        RuntimeError(
            secret_value,
        ),
        context,
    )

    assert response.status_code == 500

    assert response.data["code"] == ("INTERNAL_SERVER_ERROR")

    assert secret_value not in str(response.data)
