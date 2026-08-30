from rest_framework import serializers


class SuccessEnvelopeSerializer(serializers.Serializer):
    success = serializers.BooleanField(
        default=True,
    )

    message = serializers.CharField()

    data = serializers.JSONField(
        allow_null=True,
    )

    request_id = serializers.UUIDField(
        allow_null=True,
    )
