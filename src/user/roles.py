from django.db import models


class UserRole(models.IntegerChoices):
    DELAYED = 0, "delayed"
    USER = 1, "user"
    SALESMAN = 5, "salesman"
    ADMIN = 10, "admin"
