from .models import Category


def get_active_categories():
    return Category.objects.filter(
        is_active=True,
    ).order_by("name")


def get_category_by_id(category_id):
    return Category.objects.get(
        id=category_id,
    )