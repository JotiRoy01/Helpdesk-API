# Create your models here.
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .constants import UserRole
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Application user model.

    Email is used as the unique authentication identifier.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def is_customer(self):
        return self.role == UserRole.CUSTOMER

    @property
    def is_support_agent(self):
        return self.role == UserRole.SUPPORT_AGENT

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    role__in=[
                        UserRole.CUSTOMER,
                        UserRole.SUPPORT_AGENT,
                        UserRole.ADMIN,
                    ]
                ),
                name="valid_user_role",
            ),
        ]

    def __str__(self):
        return self.email
