from django.shortcuts import render
from apps.users.constants import UserRole
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from .filters import TicketFilter
from .permissions import (
    CanAssignTicket,
    IsAuthenticatedTicketUser,
    TicketAccessPermission,
)
from .selectors import ticket_queryset, get_ticket_for_assignment
from .serializers import (
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketTransitionSerializer,
    TicketAssignmentSerializer,
)

from .selectors import (
    get_ticket_by_id,
    get_ticket_for_update,
    get_visible_tickets_for_user,
)

from .services import create_ticket, assign_ticket
from .workflow import TicketWorkflow


class TicketListCreateView(
    generics.ListCreateAPIView
):
    permission_classes = [
        IsAuthenticatedTicketUser,
    ]

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    filterset_class = TicketFilter

    search_fields = (
        "title",
        "description",
        "category__name",
    )

    ordering_fields = (
        "created_at",
        "updated_at",
        "priority",
        "status",
        "due_at",
    )

    ordering = (
        "-created_at",
    )

    def get_queryset(self):
        return get_visible_tickets_for_user(
            user=self.request.user,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TicketCreateSerializer

        return TicketListSerializer

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
        TicketAccessPermission,
    ]

    # def get_object(self):
    #     return get_ticket_by_id(
    #         self.kwargs["pk"],
    #     )
    def get_queryset(self):
        return get_visible_tickets_for_user(
        user=self.request.user,
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

# --------------------
# assign api view
# --------------------

class TicketAssignmentView(APIView):
    permission_classes = [
        CanAssignTicket,
    ]

    def post(self, request, pk):
        serializer = TicketAssignmentSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        ticket = get_ticket_for_assignment(
            ticket_id=pk,
        )

        ticket = assign_ticket(
            ticket=ticket,
            agent=serializer.validated_data[
                "assigned_agent"
            ],
            actor=request.user,
        )

        return Response(
            {
                "message": "Ticket assigned successfully.",
                "data": TicketDetailSerializer(ticket).data,
            },
            status=status.HTTP_200_OK,
        )
