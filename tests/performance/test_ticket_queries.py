import pytest


# @pytest.mark.django_db
# def test_ticket_list_has_bounded_query_count(
#     authenticated_customer,
#     customer_ticket,
# ):
#     response = authenticated_customer.get(
#         "/api/v1/tickets/"
#     )

#     assert response.status_code == 200

@pytest.mark.django_db
def test_ticket_list_has_bounded_query_count(
    authenticated_customer,
    customer_ticket,
    django_assert_max_num_queries,
):
    with django_assert_max_num_queries(5):
        response = authenticated_customer.get(
            "/api/v1/tickets/"
        )

    assert response.status_code == 200