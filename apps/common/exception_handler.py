import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from .exceptions import ApplicationError

logger = logging.getLogger(__name__)


def _add_request_id(context, payload):
    request = context.get("request") if context else None
    payload["request_id"] = getattr(request, "request_id", None)
    return payload


def custom_exception_handler(
    exc,
    context,
):
    if isinstance(exc, ApplicationError):
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": exc.message,
                    "code": exc.code,
                    "errors": exc.errors,
                },
            ),
            status=exc.status_code,
        )

    if isinstance(exc, ValidationError):
        response = drf_exception_handler(
            exc,
            context,
        )

        data = response.data if response else None

        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "Validation failed.",
                    "code": "VALIDATION_ERROR",
                    "errors": data,
                },
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            errors = exc.message_dict
        else:
            errors = {
                "non_field_errors": exc.messages,
            }

        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "Validation failed.",
                    "code": "VALIDATION_ERROR",
                    "errors": errors,
                },
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "Authentication is required.",
                    "code": "AUTHENTICATION_REQUIRED",
                    "errors": None,
                },
            ),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, AuthenticationFailed):
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "Authentication failed.",
                    "code": "AUTHENTICATION_FAILED",
                    "errors": None,
                },
            ),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "You do not have permission to perform this action.",
                    "code": "FORBIDDEN",
                    "errors": None,
                },
            ),
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, NotFound):
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "The requested resource was not found.",
                    "code": "NOT_FOUND",
                    "errors": None,
                },
            ),
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, IntegrityError):
        logger.exception(
            "Database integrity error",
            exc_info=exc,
        )

        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "The request could not be completed.",
                    "code": "INTEGRITY_ERROR",
                    "errors": None,
                },
            ),
            status=status.HTTP_409_CONFLICT,
        )

    response = drf_exception_handler(
        exc,
        context,
    )

    if response is not None:
        return Response(
            _add_request_id(
                context,
                {
                    "success": False,
                    "message": "Request could not be completed.",
                    "code": "REQUEST_ERROR",
                    "errors": response.data,
                },
            ),
            status=response.status_code,
        )

    logger.exception(
        "Unhandled application exception",
        exc_info=exc,
        extra={
            "view": context.get("view"),
        },
    )

    return Response(
        _add_request_id(
            context,
            {
                "success": False,
                "message": "An internal server error occurred.",
                "code": "INTERNAL_SERVER_ERROR",
                "errors": None,
            },
        ),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
