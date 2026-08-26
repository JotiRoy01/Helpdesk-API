from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .permissions import IsAuthenticatedTicketUser
from .selectors import ticket_queryset
from .serializers import (
    TicketCreateSerializer,
    TicketDetailSerializer,
)
from .services import create_ticket


class TicketListCreateView(
    generics.ListCreateAPIView
):
    permission_classes = [
        IsAuthenticatedTicketUser,
    ]

    def get_queryset(self):
        return ticket_queryset()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TicketCreateSerializer

        return TicketDetailSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data

        ticket = create_ticket(
            creator=self.request.user,
            title=data["title"],
            description=data["description"],
            category=data["category"],
            priority=data["priority"],
        )

        serializer.instance = ticket


from rest_framework import generics

from .permissions import IsAuthenticatedTicketUser
from .selectors import get_ticket_by_id
from .serializers import TicketDetailSerializer


class TicketDetailView(
    generics.RetrieveUpdateAPIView
):
    serializer_class = TicketDetailSerializer
    permission_classes = [
        IsAuthenticatedTicketUser,
    ]

    def get_object(self):
        return get_ticket_by_id(
            self.kwargs["pk"],
        )