import pytest
from django.urls import reverse


@pytest.fixture(scope="function")
def get_bearer_token(api_client,user_create):
    response = api_client.post(
        reverse("user:login"),
        data={"email":"a@gmail.com", "password":"rootroot" }
    )
    print(response.data)
    return f"Bearer {response.data.get("tokens")['refresh_token']}"
