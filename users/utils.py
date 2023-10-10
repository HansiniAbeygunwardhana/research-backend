import jwt
from django.conf import settings
import datetime


def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,	
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

