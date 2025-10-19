from typing import Any

import pytest
from django.contrib.auth import get_user_model

from src.user.models import User

User = get_user_model()


@pytest.fixture(scope="function")
def user_create() -> tuple[Any, Any]:
    user = User.objects.create_user(email="a@gmail.com", password="rootroot")
    user.is_active = True
    user.save()
    return (user, user.pk)


@pytest.fixture(scope="function")
def user_model() -> type[User]:
    return User
