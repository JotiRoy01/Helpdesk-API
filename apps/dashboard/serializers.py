from rest_framework import serializers


class DashboardSummarySerializer(
    serializers.Serializer
):
    total = serializers.IntegerField()

    open = serializers.IntegerField()

    in_progress = serializers.IntegerField()

    waiting_for_user = serializers.IntegerField()

    resolved = serializers.IntegerField()

    closed = serializers.IntegerField()

    overdue = serializers.IntegerField()


class AgentWorkloadSerializer(
    serializers.Serializer
):
    id = serializers.UUIDField()

    email = serializers.EmailField()

    first_name = serializers.CharField()

    last_name = serializers.CharField()

    assigned_ticket_count = serializers.IntegerField()

    open_count = serializers.IntegerField()

    in_progress_count = serializers.IntegerField()

    waiting_for_user_count = serializers.IntegerField()

    overdue_count = serializers.IntegerField()