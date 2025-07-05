from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLES = [
        (0, "delayed"),
        (1, "user"),
        (10, "admin")
    ]
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.SmallIntegerField(default=1, choices=ROLES,
                                    validators=[MinValueValidator(0), MaxValueValidator(10)])
    last_name = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$',
                       message="Phone number must be entered in the format: '+999999999'. Допускается до 15 цифр.")])  # TODO: Change to Django-Phone-number-Field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
