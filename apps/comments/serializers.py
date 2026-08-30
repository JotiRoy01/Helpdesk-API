from rest_framework import serializers

from .models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

        fields = ("message",)

    def validate_message(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Comment message cannot be empty.")

        if len(value) > 5000:
            raise serializers.ValidationError("Comment cannot exceed 5000 characters.")

        return value


# -----------------------------------
# Create comment response serializer
# -----------------------------------


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment

        fields = (
            "id",
            "author",
            "author_name",
            "message",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_author_name(self, obj) -> str:
        return (f"{obj.author.first_name} {obj.author.last_name}").strip()
