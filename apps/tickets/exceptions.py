from apps.common.exceptions import (
    ConflictError,
    DomainPermissionError,
    DomainValidationError,
    ResourceNotFoundError,
)


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
