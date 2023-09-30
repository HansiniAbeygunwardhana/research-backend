from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response	
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_access_token

# Create your views here.

class JWTLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        response = Response()

        token = generate_access_token(user)
        response.set_cookie(key="jwt", value=token, httponly=True)

        response.data = {
            "jwt": token,
        }

        return response
    
#view to create users
class RegisterView(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if User.objects.filter(username=username).exists():
            raise AuthenticationFailed("Username already exists!")
        if User.objects.filter(email=email).exists():
            raise AuthenticationFailed("Email already exists!")
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({"message": "User created successfully!"})
    
    
#view to logout users
class LogoutView(APIView):
    
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response

#view to reset password
class ResetPasswordView(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            return Response({"message": "Password reset success!"})
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        