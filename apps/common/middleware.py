import uuid


class RequestIDMiddleware:
    """
    Adds a unique ID to each request for tracing.

    The ID is returned to the client and can be correlated
    with server logs.
    """

    HEADER_NAME = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get(
            self.HEADER_NAME
        ) or str(uuid.uuid4())

        request.request_id = request_id

        response = self.get_response(request)

        response[self.HEADER_NAME] = request_id

        return response