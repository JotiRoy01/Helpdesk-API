from django.db import transaction

from .models import Category


@transaction.atomic
def create_category(
    *,
    name,
    description="",
):
    return Category.objects.create(
        name=name.strip(),
        description=description.strip(),
    )


@transaction.atomic
def update_category(
    *,
    category,
    data,
):
    if "name" in data:
        category.name = data["name"].strip()

    if "description" in data:
        category.description = data["description"].strip()

    if "is_active" in data:
        category.is_active = data["is_active"]

    category.save()

    return category