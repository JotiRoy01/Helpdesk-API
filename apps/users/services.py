from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


@transaction.atomic
def register_user(
    *,
    email,
    first_name,
    last_name,
    password,
):
    user = User.objects.create_user(
        email=email,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        password=password,
    )

    return user


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def update_last_login(user):
    user.last_login = timezone.now()

    user.save(
        update_fields=[
            "last_login",
        ]
    )