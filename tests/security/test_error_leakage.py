import pytest


@pytest.mark.django_db
def test_internal_error_does_not_expose_exception(
    api_client,
    customer,
    monkeypatch,
):
    from apps.tickets import views

    secret = "SUPER_SECRET_DATABASE_PASSWORD"

    def exploding_queryset(self):
        raise RuntimeError(secret)

    monkeypatch.setattr(
        views.TicketListCreateView,
        "get_queryset",
        exploding_queryset,
    )

    api_client.force_authenticate(user=customer)

    response = api_client.get(
        "/api/v1/tickets/",
    )

    assert response.status_code == 500

    response_text = str(response.data)

    assert secret not in response_text
    assert "Traceback" not in response_text
