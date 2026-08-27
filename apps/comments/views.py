from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Comment
from .permissions import CanAccessTicketComments
from .selectors import get_comments_for_ticket, get_visible_ticket_by_id
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
)
from .services import create_comment

class TicketCommentListCreateView(
    generics.ListCreateAPIView
):
    def get_ticket(self):
        return get_visible_ticket_by_id(
            ticket_id=self.kwargs["ticket_id"],
            user=self.request.user,
        )

    def get_queryset(self):
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

            raise PermissionDenied(
                permission.message
            )

        create_comment(
            ticket=ticket,
            author=self.request.user,
            message=serializer.validated_data[
                "message"
            ],
        )