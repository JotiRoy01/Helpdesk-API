from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthenticatedTicketUser
from .selectors import ticket_queryset
from .serializers import (
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketTransitionSerializer
)
from .services import create_ticket
from .workflow import TicketWorkflow


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


class TicketTransitionView(APIView):
    permission_classes = [
        IsAuthenticatedTicketUser,
    ]

    def post(self, request, pk):
        serializer = TicketTransitionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        ticket = get_ticket_by_id(pk)

        ticket = TicketWorkflow.transition(
            ticket=ticket,
            new_status=serializer.validated_data["status"],
            actor=request.user,
        )

        return Response(
            TicketDetailSerializer(ticket).data,
            status=status.HTTP_200_OK,
        )