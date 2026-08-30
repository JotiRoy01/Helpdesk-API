from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(
        default=False,
    )

    message = serializers.CharField()

    code = serializers.CharField()

    errors = serializers.JSONField(
        allow_null=True,
    )

    request_id = serializers.CharField(
        allow_null=True,
    )
