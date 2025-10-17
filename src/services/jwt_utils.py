from datetime import datetime, timedelta

import jwt

from django.conf import settings


def jwt_generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now() + timedelta(days=14),
        "iat": datetime.now()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def jwt_verification_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_auth_tokens(user_id) -> dict[str, str]:
    payload_access = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(hours=1),
        "iat": datetime.now()
    }
    payload_refresh = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=14),
        "iat": datetime.now()
    }

    token_access = jwt.encode(payload_access, settings.SECRET_KEY, algorithm="HS256")
    token_refresh = jwt.encode(payload_refresh, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token_access, "refresh_token": token_refresh}
