class ApplicationError(Exception):
    """
    Base class for expected application/domain errors.
    """

    status_code = 400
    default_code = "APPLICATION_ERROR"
    default_message = "An application error occurred."

    def __init__(
        self,
        message=None,
        *,
        code=None,
        status_code=None,
        errors=None,
    ):
        super().__init__(message or self.default_message)

        self.message = message or self.default_message
        self.code = code or self.default_code
        self.status_code = status_code if status_code is not None else self.status_code
        self.errors = errors


class ResourceNotFoundError(ApplicationError):
    status_code = 404
    default_code = "RESOURCE_NOT_FOUND"
    default_message = "The requested resource was not found."


class DomainValidationError(ApplicationError):
    status_code = 400
    default_code = "DOMAIN_VALIDATION_ERROR"
    default_message = "The requested operation is invalid."


class DomainPermissionError(ApplicationError):
    status_code = 403
    default_code = "FORBIDDEN"
    default_message = "You do not have permission to perform this action."


class ConflictError(ApplicationError):
    status_code = 409
    default_code = "CONFLICT"
    default_message = "The requested operation conflicts with the current state."


class TicketNotFoundError(ResourceNotFoundError):
    default_code = "TICKET_NOT_FOUND"
    default_message = "Ticket not found."


class InvalidTicketTransitionError(DomainValidationError):
    default_code = "INVALID_TICKET_TRANSITION"
    default_message = "The requested ticket transition is not allowed."


class TicketAccessDeniedError(DomainPermissionError):
    default_code = "TICKET_ACCESS_DENIED"
    default_message = "You do not have permission to access this ticket."


class TicketAssignmentError(DomainValidationError):
    default_code = "INVALID_TICKET_ASSIGNMENT"
    default_message = "The ticket cannot be assigned as requested."


class TicketStateConflictError(ConflictError):
    default_code = "TICKET_STATE_CONFLICT"
    default_message = "The ticket state has changed. Please retry."
