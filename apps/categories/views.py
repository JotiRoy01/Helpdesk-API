from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Category
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer


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


class CategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]