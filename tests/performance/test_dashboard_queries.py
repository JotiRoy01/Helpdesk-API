import pytest

from apps.tickets.models import Ticket


@pytest.mark.django_db
def test_dashboard_summary_uses_bounded_queries(
    authenticated_admin,
    django_assert_max_num_queries,
):
    with django_assert_max_num_queries(3):
        response = authenticated_admin.get(
            "/api/v1/dashboard/summary/"
        )

    assert response.status_code == 200



@pytest.mark.django_db
def test_dashboard_workload_avoids_n_plus_one(
    authenticated_admin,
    agent,
    another_agent,
    django_assert_max_num_queries,
):
    with django_assert_max_num_queries(3):
        response = authenticated_admin.get(
            "/api/v1/dashboard/workload/"
        )

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.performance
def test_ticket_list_pagination_and_filters(
    authenticated_customer,
    category,
    customer,
):
    for index in range(100):
        Ticket.objects.create(
            title=f"Ticket {index}",
            description="Test ticket description.",
            category=category,
            creator=customer,
        )

    response = authenticated_customer.get(
        "/api/v1/tickets/?page_size=20"
    )
    assert len(response.data["results"]) <= 20

    response = authenticated_customer.get(
        "/api/v1/tickets/?page_size=100000"
    )
    assert len(response.data["results"]) <= 100

    response = authenticated_customer.get(
        "/api/v1/tickets/?ordering=password"
    )
    assert response.status_code == 200

    response = authenticated_customer.get(
        "/api/v1/tickets/",
        {
            "status": "OPEN",
            "priority": "HIGH",
            "search": "VPN",
            "ordering": "-created_at",
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200
    assert len(response.data["results"]) <= 20