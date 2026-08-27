from rest_framework.response import Response


def success_response(
    *,
    data=None,
    message="Success.",
    status_code=200,
    request_id=None,
):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "request_id": request_id,
        },
        status=status_code,
    )


def error_response(
    *,
    message,
    code,
    errors=None,
    status_code=400,
    request_id=None,
):
    return Response(
        {
            "success": False,
            "message": message,
            "code": code,
            "errors": errors,
            "request_id": request_id,
        },
        status=status_code,
    )