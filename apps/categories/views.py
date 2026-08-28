from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Category
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Categories"],
    summary="List and create categories",
)
# class CategoryListCreateView(
#     generics.ListCreateAPIView
# ):
class CategoryListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Category.objects.all()

        if self.request.method == "GET":
            queryset = queryset.filter(
                is_active=True,
            )

        return queryset

@extend_schema(
    tags=["Categories"],
    summary="Retrieve or update a category",
)
# class CategoryDetailView(
#     generics.RetrieveUpdateAPIView
# ):
class CategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]