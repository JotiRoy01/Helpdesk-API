def test_customer_cannot_access_other_customer_ticket(
    api_client,
    customer,
    another_customer,
    category,
):
    from apps.tickets.models import Ticket

    other_ticket = Ticket.objects.create(
        title="Private ticket",
        description="Private issue.",
        category=category,
        creator=another_customer,
    )

    api_client.force_authenticate(
        user=customer,
    )

    response = api_client.get(
        f"/api/v1/tickets/{other_ticket.id}/",
    )

    assert response.status_code == 404



def test_customer_cannot_comment_on_other_customer_ticket(
    api_client,
    customer,
    another_customer,
    category,
):
    from apps.tickets.models import Ticket

    other_ticket = Ticket.objects.create(
        title="Private ticket",
        description="Private issue.",
        category=category,
        creator=another_customer,
    )

    api_client.force_authenticate(
        user=customer,
    )

    response = api_client.post(
        f"/api/v1/tickets/{other_ticket.id}/comments/",
        {
            "message": "Unauthorized comment.",
        },
        format="json",
    )

    assert response.status_code == 404