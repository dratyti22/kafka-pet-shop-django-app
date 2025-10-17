import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="function")
def user_create() -> User:
    user = User.objects.create_user(email="a@gmail.com", password="rootroot")
    user.is_active = True
    user.save()
    return user


@pytest.fixture(scope="function")
def user_model() -> type[User]:
    return User
