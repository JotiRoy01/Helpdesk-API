import pytest

from apps.tickets.constants import TicketStatus
from apps.tickets.workflow import TicketWorkflow

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("current", "new", "allowed"),
    [
        (
            TicketStatus.OPEN,
            TicketStatus.IN_PROGRESS,
            True,
        ),
        (
            TicketStatus.OPEN,
            TicketStatus.RESOLVED,
            False,
        ),
        (
            TicketStatus.IN_PROGRESS,
            TicketStatus.WAITING_FOR_USER,
            True,
        ),
        (
            TicketStatus.IN_PROGRESS,
            TicketStatus.RESOLVED,
            True,
        ),
        (
            TicketStatus.WAITING_FOR_USER,
            TicketStatus.IN_PROGRESS,
            True,
        ),
        (
            TicketStatus.RESOLVED,
            TicketStatus.CLOSED,
            True,
        ),
        (
            TicketStatus.CLOSED,
            TicketStatus.OPEN,
            False,
        ),
    ],
)
def test_transition_matrix(
    current,
    new,
    allowed,
):
    if allowed:
        TicketWorkflow.validate_transition(
            current_status=current,
            new_status=new,
        )
    else:
        with pytest.raises(Exception):
            TicketWorkflow.validate_transition(
                current_status=current,
                new_status=new,
            )