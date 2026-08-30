# Create your views here.
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics

from .models import Comment
from .permissions import CanAccessTicketComments
from .selectors import get_comments_for_ticket, get_visible_ticket_by_id
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
)
from .services import create_comment


@extend_schema_view(
    get=extend_schema(
        tags=["Comments"],
        summary="List ticket comments",
        description=(
            "Returns comments for a ticket visible to the authenticated user."
        ),
        responses=CommentSerializer,
    ),
    post=extend_schema(
        tags=["Comments"],
        summary="Add ticket comment",
        description=(
            "Adds a comment to a ticket. The author is always the authenticated user."
        ),
        request=CommentCreateSerializer,
        responses={
            201: CommentSerializer,
            400: OpenApiResponse(description="Validation error."),
            404: OpenApiResponse(description="Ticket not found."),
        },
    ),
)
# class TicketCommentListCreateView(
#     generics.ListCreateAPIView
# ):
class TicketCommentListCreateView(generics.ListCreateAPIView):
    def get_ticket(self):
        return get_visible_ticket_by_id(
            ticket_id=self.kwargs["ticket_id"],
            user=self.request.user,
        )

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()

        ticket = self.get_ticket()

        return get_comments_for_ticket(
            ticket_id=ticket.id,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer

        return CommentSerializer

    def perform_create(self, serializer):
        ticket = self.get_ticket()

        permission = CanAccessTicketComments()

        if not permission.has_object_permission(
            self.request,
            self,
            ticket,
        ):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(permission.message)

        create_comment(
            ticket=ticket,
            author=self.request.user,
            message=serializer.validated_data["message"],
        )
