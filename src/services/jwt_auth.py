from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import ExpiredTokenError, InvalidToken, TokenError

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            user = verify_token_from_headers(request)
            return (user, None)
        except (TokenError, ExpiredTokenError, InvalidToken):
            return None


def verify_token_from_headers(request: Request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        raise TokenError("Not token")

    parts = auth_header.split()
    if len(parts) != 2:
        raise TokenError("Invalid token format")

    token_type, token = parts
    if token_type != "Bearer":
        raise TokenError("Token must start with Bearer")

    return verify_access_token(token)


def verify_access_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise ExpiredTokenError

    user_id = payload.get("user_id")
    if not user_id:
        raise TokenError

    try:
        user = User.objects.get(pk=user_id)
        return user
    except User.DoesNotExist:
        return None
