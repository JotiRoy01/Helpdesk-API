# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.responses import success_response

from .filters import TicketFilter
from .models import Ticket
from .permissions import (
    CanAssignTicket,
    CanTransitionTicket,
    IsAuthenticatedTicketUser,
    TicketAccessPermission,
)
from .selectors import (
    get_ticket_for_assignment,
    get_visible_ticket_by_id,
    get_visible_tickets_for_user,
)
from .serializers import (
    TicketAssignmentResponseSerializer,
    TicketAssignmentSerializer,
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketTransitionSerializer,
    TicketUpdateSerializer,
)
from .services import assign_ticket, create_ticket
from .workflow import TicketWorkflow


@extend_schema(
    tags=["Tickets"],
    summary="List or create tickets",
    description=(
        "Returns tickets visible to the authenticated "
        "user according to role and ownership rules. "
        "Supports filtering, search, ordering, and pagination."
    ),
    parameters=[
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter by ticket status.",
        ),
        OpenApiParameter(
            name="priority",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter by ticket priority.",
        ),
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="Filter by category UUID.",
        ),
        OpenApiParameter(
            name="assigned_agent",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="Filter by assigned agent UUID.",
        ),
        OpenApiParameter(
            name="creator",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="Filter by creator UUID.",
        ),
        OpenApiParameter(
            name="is_overdue",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter overdue tickets.",
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=("Search title, description, or category name."),
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=(
                "Ordering: created_at, updated_at, "
                "priority, status, due_at. "
                "Prefix with '-' for descending order."
            ),
        ),
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="page_size",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
    ],
)
# class TicketListCreateView(
#     generics.ListCreateAPIView
# ):
class TicketListCreateView(generics.ListCreateAPIView):
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

    ordering = ("-created_at",)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Ticket.objects.none()

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
            ip_address=self.request.META.get("REMOTE_ADDR"),
            user_agent=self.request.META.get(
                "HTTP_USER_AGENT",
                "",
            ),
        )

        serializer.instance = ticket

    @extend_schema(
        request=TicketCreateSerializer,
        responses={201: TicketDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_response(
            data=TicketDetailSerializer(serializer.instance).data,
            message="Ticket created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Tickets"],
    summary="Retrieve a ticket",
    description=(
        "Returns a ticket visible to the authenticated "
        "user according to role and ownership."
    ),
    responses={
        200: TicketDetailSerializer,
        404: OpenApiResponse(description="Ticket not found."),
    },
)
# class TicketDetailView(
#     generics.RetrieveUpdateAPIView
# ):
class TicketDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [
        IsAuthenticatedTicketUser,
        TicketAccessPermission,
    ]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Ticket.objects.none()

        return get_visible_tickets_for_user(
            user=self.request.user,
        )

    def get_object(self):
        """Return a visible ticket with a ticket-specific 404 error."""
        return get_visible_ticket_by_id(
            ticket_id=self.kwargs["pk"],
            user=self.request.user,
        )

    def get_serializer_class(self):
        if self.request.method in {
            "PUT",
            "PATCH",
        }:
            return TicketUpdateSerializer

        return TicketDetailSerializer


@extend_schema(
    tags=["Ticket Workflow"],
    summary="Transition ticket status",
    description=(
        "Transitions a ticket through the allowed "
        "support workflow. Customers cannot perform "
        "workflow transitions. Support agents may "
        "transition tickets assigned to them. "
        "Only administrators can close tickets."
    ),
    request=TicketTransitionSerializer,
    responses={
        200: TicketDetailSerializer,
        400: OpenApiResponse(description="Invalid transition."),
        403: OpenApiResponse(description="Workflow permission denied."),
        404: OpenApiResponse(description="Ticket not found."),
    },
)
# class TicketTransitionView(APIView):
class TicketTransitionView(APIView):
    permission_classes = [
        CanTransitionTicket,
    ]

    @extend_schema(
        request=TicketTransitionSerializer,
        responses={200: TicketDetailSerializer},
    )
    def post(self, request, pk):
        serializer = TicketTransitionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        ticket = get_visible_ticket_by_id(
            ticket_id=pk,
            user=request.user,
        )

        ticket = TicketWorkflow.transition(
            ticket=ticket,
            new_status=serializer.validated_data["status"],
            actor=request.user,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        return Response(
            TicketDetailSerializer(ticket).data,
            status=status.HTTP_200_OK,
        )


# --------------------
# assign api view
# --------------------


@extend_schema(
    tags=["Ticket Assignment"],
    summary="Assign ticket to support agent",
    description=(
        "Assigns or reassigns a ticket to an active "
        "Support Agent. Only administrators can perform "
        "this operation."
    ),
    request=TicketAssignmentSerializer,
    responses={
        200: TicketAssignmentResponseSerializer,
        400: OpenApiResponse(description="Invalid assignment."),
        403: OpenApiResponse(description="Administrator access required."),
        404: OpenApiResponse(description="Ticket not found."),
    },
)
# class TicketAssignmentView(APIView):


class TicketAssignmentView(APIView):
    permission_classes = [
        CanAssignTicket,
    ]

    @extend_schema(
        request=TicketAssignmentSerializer,
        responses={200: TicketDetailSerializer},
    )
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
            agent=serializer.validated_data["assigned_agent"],
            actor=request.user,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        return Response(
            {
                "message": "Ticket assigned successfully.",
                "data": TicketDetailSerializer(ticket).data,
            },
            status=status.HTTP_200_OK,
        )
