import pytest

from django.db import transaction

from apps.tickets.selectors import (
    get_ticket_for_assignment,
)


@pytest.mark.django_db(transaction=True)
def test_ticket_row_can_be_locked(
    ticket,
):
    with transaction.atomic():
        locked_ticket = get_ticket_for_assignment(
            ticket_id=ticket.id,
        )

        assert locked_ticket.id == ticket.id