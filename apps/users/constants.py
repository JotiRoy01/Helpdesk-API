from django.db import models


class UserRole(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer"
    SUPPORT_AGENT = "SUPPORT_AGENT", "Support Agent"
    ADMIN = "ADMIN", "Admin"