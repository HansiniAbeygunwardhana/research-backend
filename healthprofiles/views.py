from django.shortcuts import render , get_object_or_404
from .models import HealthProfile
from .serializer import HealthProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from users.authentication import JWTAuthentication
from django.db import IntegrityError

# Create your views here.
class HealthProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        user = request.user
        if user is None:
            return Response({"message" : "User not found"} , status=status.HTTP_404_NOT_FOUND)
        healthprofile = get_object_or_404(HealthProfile , user = user)
        if healthprofile :
            serializer = HealthProfileSerializer(healthprofile)
            return Response(serializer.data)
        else :
            return Response({"message" : "HealthProfile not found"} , status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        user = request.user
        serializer = HealthProfileSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Instead of calling serializer.save(), call the perform_create method
                self.perform_create(serializer, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response(
                {"message": "Health profile already exists for this user."},
                status=status.HTTP_409_CONFLICT,
            )

    def perform_create(self, serializer , user):
        # Automatically set the user field to the authenticated user
        serializer.save(user=user)
    
    def delete(self , request):
        healthprofiles = HealthProfile.objects.all()
        if healthprofiles:
            healthprofiles.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)