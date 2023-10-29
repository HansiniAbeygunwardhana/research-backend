from django.shortcuts import render , get_object_or_404
from .models import HealthProfile
from .serializer import HealthProfileSerializer , UserProfileAndHealthProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from users.authentication import JWTAuthentication
from django.db import IntegrityError
from recommandation.models import UserProfile

# Create your views here.
class HealthProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer = UserProfileAndHealthProfileSerializer
    
    def get(self, request):
            user = request.user
            if user is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            healthprofile = HealthProfile.objects.filter(user=user).first()
            userprofile = UserProfile.objects.filter(user=user).first()

            if healthprofile is not None and userprofile is not None:
                data = {
                    'userprofile': userprofile,
                    'healthprofile': healthprofile,
                }
                serializer = UserProfileAndHealthProfileSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "HealthProfile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        user = request.user
        serializer = UserProfileAndHealthProfileSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Extract the userprofile data from the serializer data
                userprofile_data = serializer.validated_data.pop('userprofile')
                health_profile_data = serializer.validated_data.pop('healthprofile')

                # Create or update the user's UserProfile
                user_profile, created = UserProfile.objects.update_or_create(
                    user=user , defaults=userprofile_data
                )
                
                print(user_profile.user.id)

                # Create or update the user's HealthProfile
                health_profile, created = HealthProfile.objects.update_or_create(
                    user=user, defaults=health_profile_data
                )

                print(health_profile)    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(e)
            return Response(
                {"message": "Health profile already exists for this user."},
                status=status.HTTP_409_CONFLICT,
            )

    def perform_create(self, serializer):
        # Get the username from the JWT token
        username = self.request.user.username

        # Set the username in the serializer
        serializer.validated_data['username'] = username

        # Save the serializer instance
        serializer.save()
    
    def delete(self , request):
        user = request.user
        healthprofiles = HealthProfile.objects.filter(user=user).first()
        userprofiles = UserProfile.objects.filter(user=user).first()
        if healthprofiles is not None and userprofiles is not None:
            healthprofiles.delete()
            userprofiles.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        user = request.user
        health_profile = HealthProfile.objects.filter(user=user).first()
        if health_profile is None:
            return Response({"message": "HealthProfile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileAndHealthProfileSerializer(
            instance=health_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            # Update the user's UserProfile
            userprofile_data = serializer.validated_data.pop('userprofile')
            for key, value in userprofile_data.items():
                setattr(user.profile, key, value)
            user.profile.save()

            # Update the user's HealthProfile
            for key, value in serializer.validated_data.items():
                setattr(health_profile, key, value)
            health_profile.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)