from django.contrib.auth.base_user import BaseUserManager

from .constants import UserRole


class UserManager(BaseUserManager):
    """
    Custom manager for the application User model.

    Email is the primary authentication identifier.
    """

    use_in_migrations = True

    def create_user(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        extra_fields["role"] = UserRole.ADMIN

        if not extra_fields["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")

        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
