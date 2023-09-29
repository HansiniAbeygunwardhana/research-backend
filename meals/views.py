from django.shortcuts import render
from rest_framework.views import APIView
from .models import Meal , keyword , ingredient
from .serializers import MealSerializer , keywordSerializer , ingredientSerializer
from rest_framework import viewsets , status
from rest_framework.response import Response

# Create your views here.
class MealView(APIView):
    def get(self , request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "New meal added"} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request):
        meals = Meal.objects.all()
        if meals:
            meals.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)