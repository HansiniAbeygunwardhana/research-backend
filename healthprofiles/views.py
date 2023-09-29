from django.shortcuts import render
from .models import HealthProfile
from .serializer import HealthProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class HealthProfileView(APIView):
    def get(self, request):
        healthprofiles = HealthProfile.objects.all()
        serializer = HealthProfileSerializer(healthprofiles, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = HealthProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request):
        healthprofiles = HealthProfile.objects.all()
        if healthprofiles:
            healthprofiles.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)