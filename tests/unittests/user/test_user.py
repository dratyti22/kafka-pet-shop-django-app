# tests/unittests/user/test_user.py
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.api
@pytest.mark.user
class TestUserApi:
    def test_user_login(self, api_client, user_create):
        res = api_client.post(
            reverse("user:login"),
            data={"email": "a@gmail.com", "password": "rootroot"},
        )

        assert res.status_code == 200
        assert "access_token" in res.data.get("tokens")
        assert "refresh_token" in res.data.get("tokens")

    def test_user_login_wrong_password(self, api_client, user_create):
        res = api_client.post(
            reverse("user:login"),
            data={"email": "a@gmail.com", "password": "wrongpassword"},
        )
        assert res.status_code == 401

    def test_user_register(self, api_client):
        res = api_client.post(
            reverse("user:register"),
            data={
                "email": "newuser@example.com",
                "password": "newpassword123",
                "password2": "newpassword123"
            },
        )
        assert res.status_code == 201

    def test_logout_user(self, api_client, get_bearer_token):
        api_client.credentials(HTTP_AUTHORIZATION=get_bearer_token)
        res = api_client.get(reverse("user:logout"))
        assert res.status_code == 200

    def test_get_me_user(self, api_client, get_bearer_token):
        api_client.credentials(HTTP_AUTHORIZATION=get_bearer_token)
        res = api_client.get(reverse("user:profile-me-list"))
        print(res.data)
        assert res.status_code == 200

    def test_me_user_update(self, api_client, get_bearer_token, user_create):
        _, pk = user_create
        api_client.credentials(HTTP_AUTHORIZATION=get_bearer_token)
        res = api_client.patch(reverse("user:profile-me-detail", kwargs={"pk": pk}), {"phone": "+7 935 738 61 73", "last_name": "Dratyti", "first_name": "Dratyti"})

        assert res.status_code == 200

