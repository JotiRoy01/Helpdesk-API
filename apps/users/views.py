from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .services import (
    generate_tokens,
    update_last_login,
)


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        email = (request.data or {}).get("email")

        if email:
            return self.cache_format % {
                "scope": self.scope,
                "ident": email.strip().lower(),
            }

        return super().get_cache_key(request, view)

    def allow_request(self, request, view):
        if request.method != "POST":
            return True

        email = (request.data or {}).get("email")
        password = (request.data or {}).get("password")

        if not email or not password:
            return True

        from django.contrib.auth import authenticate

        if authenticate(email=email, password=password) is not None:
            return True

        return super().allow_request(request, view)

# Registration
class RegisterView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        return Response(
            {
                "message": "Account created successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    throttle_classes = [LoginRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data["user"]

        tokens = generate_tokens(user)

        update_last_login(user)

        return Response(
            {
                "message": "Login successful.",
                "data": {
                    "user": UserSerializer(user).data,
                    "tokens": tokens,
                },
            },
            status=status.HTTP_200_OK,
        )

# Current-user endpoint
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "data": UserSerializer(
                    request.user
                ).data,
            }
        )

# Logout endpoint

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get(
            "refresh",
        )

        if not refresh_token:
            return Response(
                {
                    "message": (
                        "Refresh token is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            return Response(
                {
                    "message": (
                        "Invalid or expired refresh token."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "token_refresh"