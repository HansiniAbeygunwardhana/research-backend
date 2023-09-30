from django.http import HttpRequest
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        token = self.get_token_from_header(request)
        if token is None:
            return None
        
        try :
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            return (user, None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token Expired!")
        except jwt.DecodeError:
            raise AuthenticationFailed("Token Invalid!")
    
    
    def get_token_from_header(self, request : HttpRequest):
        header = request.headers.get("Authorization")
        
        if header and header.startswith("Bearer"):
            return header.split(" ")[1]
        return None