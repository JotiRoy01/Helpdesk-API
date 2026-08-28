from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers

from .constants import UserRole
from .models import User
from .services import register_user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "created_at",
        )

        read_only_fields = (
            "id",
            "role",
            "is_active",
            "created_at",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    password_confirmation = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    class Meta:
        model = User

        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
        )

    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    def validate(self, attrs):
        password = attrs["password"]

        if password != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {
                    "password_confirmation": (
                        "Passwords do not match."
                    )
                }
            )

        password_validation.validate_password(
            password,
        )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmation")

        return User.objects.create_user(
            #role=UserRole.CUSTOMER,
            **validated_data,
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        attrs["user"] = user

        return attrs


class RegisterResponseSerializer(
    serializers.Serializer
):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = UserSerializer()
    request_id = serializers.CharField(
        allow_null=True,
    )


class TokenPairSerializer(
    serializers.Serializer
):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginDataSerializer(
    serializers.Serializer
):
    user = UserSerializer()
    tokens = TokenPairSerializer()


class LoginResponseSerializer(
    serializers.Serializer
):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = LoginDataSerializer()
    request_id = serializers.CharField(
        allow_null=True,
    )