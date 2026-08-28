def test_customer_cannot_assign_ticket(
    api_client,
    customer,
    agent,
    customer_ticket,
):
    api_client.force_authenticate(
        user=customer,
    )

    response = api_client.post(
        f"/api/v1/tickets/{customer_ticket.id}/assign/",
        {
            "assigned_agent": str(agent.id),
        },
        format="json",
    )

    assert response.status_code == 403



def test_customer_cannot_close_ticket(
    api_client,
    customer_ticket,
    customer,
):
    api_client.force_authenticate(
        user=customer,
    )

    response = api_client.post(
        f"/api/v1/tickets/{customer_ticket.id}/transition/",
        {
            "status": "CLOSED",
        },
        format="json",
    )

    assert response.status_code == 403