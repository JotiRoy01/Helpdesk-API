import pytest

from apps.comments.models import Comment


@pytest.mark.django_db
def test_comment_list_has_bounded_queries(
    api_client,
    customer,
    customer_ticket,
    django_assert_max_num_queries,
):
    for index in range(10):
        Comment.objects.create(
            ticket=customer_ticket,
            author=customer,
            message=f"Comment {index}",
        )

    api_client.force_authenticate(
        user=customer,
    )

    with django_assert_max_num_queries(5):
        response = api_client.get(
            f"/api/v1/tickets/{customer_ticket.id}/comments/"
        )

    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_list_does_not_have_n_plus_one(
    api_client,
    customer,
    customer_ticket,
    django_assert_max_num_queries,
):
    for index in range(10):
        Comment.objects.create(
            ticket=customer_ticket,
            author=customer,
            message=f"Comment {index}",
        )

    api_client.force_authenticate(
        user=customer,
    )

    with django_assert_max_num_queries(5):
        response = api_client.get(
            f"/api/v1/tickets/{customer_ticket.id}/comments/"
        )

    assert response.status_code == 200