from django.db import models


class UserRole(models.IntegerChoices):
    DELAYED = 0, "delayed"
    USER = 1, "user"
    ADMIN = 10, "admin"
