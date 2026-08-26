from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )