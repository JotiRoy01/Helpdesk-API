import pytest

from apps.categories.services import (
    create_category,
    update_category,
)


@pytest.mark.django_db
def test_create_category():
    category = create_category(
        name="Hardware",
        description="Hardware support.",
    )

    assert category.name == "Hardware"
    assert category.is_active is True


@pytest.mark.django_db
def test_deactivate_category():
    category = create_category(
        name="Software",
    )

    update_category(
        category=category,
        data={
            "is_active": False,
        },
    )

    category.refresh_from_db()

    assert category.is_active is False
