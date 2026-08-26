import pytest

from apps.categories.serializers import CategorySerializer


@pytest.mark.django_db
def test_category_name_is_trimmed():
    serializer = CategorySerializer(
        data={
            "name": "  Network  ",
            "description": "Network issues.",
        }
    )

    assert serializer.is_valid(), serializer.errors

    assert serializer.validated_data["name"] == "Network"