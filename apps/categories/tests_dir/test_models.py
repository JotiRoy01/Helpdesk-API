import pytest

from apps.categories.models import Category


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(
        name="Network",
        description="Network-related issues.",
    )

    assert category.name == "Network"
    assert category.is_active is True