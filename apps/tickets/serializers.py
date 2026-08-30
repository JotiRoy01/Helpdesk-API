from rest_framework import serializers

from apps.categories.models import Category
from apps.users.constants import UserRole
from apps.users.models import User

from .constants import TicketStatus
from .models import Ticket
from .overdue import OverdueTicketService


class TicketCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
    )

    class Meta:
        model = Ticket

        fields = (
            "title",
            "description",
            "category",
            "priority",
        )

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must contain at least 5 characters."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must contain at least 10 characters."
            )

        return value


class TicketDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    creator_name = serializers.SerializerMethodField()

    assigned_agent_name = serializers.SerializerMethodField()

    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Ticket

        fields = (
            "id",
            "title",
            "description",
            "category",
            "category_name",
            "priority",
            "status",
            "creator",
            "creator_name",
            "assigned_agent",
            "assigned_agent_name",
            "due_at",
            "is_overdue",
            "resolved_at",
            "closed_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_creator_name(self, obj) -> str:
        return (f"{obj.creator.first_name} {obj.creator.last_name}").strip()

    def get_assigned_agent_name(self, obj) -> str | None:
        if not obj.assigned_agent:
            return None

        return (
            f"{obj.assigned_agent.first_name} {obj.assigned_agent.last_name}"
        ).strip()

    def get_is_overdue(self, obj) -> bool:
        # from django.utils import timezone

        # if not obj.due_at:
        #     return False

        # if obj.status in {
        #     TicketStatus.RESOLVED,
        #     TicketStatus.CLOSED,
        # }:
        #     return False

        # return timezone.now() > obj.due_at
        return OverdueTicketService.is_overdue(
            ticket=obj,
        )


class TicketTransitionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=TicketStatus.choices,
    )

    def validate_status(self, value):
        if value == TicketStatus.OPEN:
            return value

        return value


class TicketAssignmentSerializer(serializers.Serializer):
    assigned_agent = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    def validate_assigned_agent(self, user):
        if user.role != UserRole.SUPPORT_AGENT:
            raise serializers.ValidationError(
                "Tickets can only be assigned to support agents."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Cannot assign a ticket to an inactive agent."
            )

        return user


# ---------------------
# ---------------------
class TicketAssignmentResponseSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket

        fields = (
            "id",
            "assigned_agent",
            "assigned_agent_name",
            "updated_at",
        )

    def get_assigned_agent_name(self, obj) -> str | None:
        if not obj.assigned_agent:
            return None

        return (
            f"{obj.assigned_agent.first_name} {obj.assigned_agent.last_name}"
        ).strip()


# -------------------------------
# Add a dedicated list serializer
# -------------------------------
class TicketListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    assigned_agent_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket

        fields = (
            "id",
            "title",
            "category",
            "category_name",
            "priority",
            "status",
            "assigned_agent",
            "assigned_agent_name",
            "due_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_assigned_agent_name(self, obj) -> str | None:
        if not obj.assigned_agent:
            return None

        return (
            f"{obj.assigned_agent.first_name} {obj.assigned_agent.last_name}"
        ).strip()


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket

        fields = (
            "title",
            "description",
            "category",
            "priority",
        )

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must contain at least 5 characters."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must contain at least 10 characters."
            )

        return value
