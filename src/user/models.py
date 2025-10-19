import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from src.user.managers import CustomUserManager
from src.user.roles import UserRole


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    username = models.CharField(max_length=150, unique=True, null=True, blank=True, default=None)
    email = models.EmailField(_('email address'), unique=True)
    role = models.SmallIntegerField(default=UserRole.USER, choices=UserRole.choices,
                                    validators=[MinValueValidator(0), MaxValueValidator(10)])
    last_name = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True, region="RU")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["email"])
        ]
        ordering = ["id", "email"]

    def __str__(self):
        return f"{self.email}-{self.role}"
