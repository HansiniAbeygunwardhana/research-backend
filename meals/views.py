from django.shortcuts import render
from rest_framework.views import APIView
from .models import Meal , keyword , ingredient
from .serializers import MealSerializer , MealSerializerBasic , MealSerializerExtended , KeywordSerialiserBasic
from rest_framework import viewsets , status
from rest_framework.response import Response

# Create your views here.
class MealView(APIView):
    def get(self , request , pk=None):
        if pk:
            meal = Meal.objects.get(id=pk)
            if meal:
                serializer = MealSerializerExtended(meal)
                return Response(serializer.data)
            else:
                return Response({"message" : "Meal not found"} , status=status.HTTP_404_NOT_FOUND)
        else:
            meals = Meal.objects.all()
            serializer = MealSerializerBasic(meals , many=True)
            return Response(serializer.data)
    
    
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
        

class KeywordView(APIView):
    def get(self , request):
        try:
            keywords = keyword.objects.all()
            if keywords:
                serializer = KeywordSerialiserBasic(keywords , many=True)
                return Response(serializer.data)
            else :
                return Response({"message : No Data"} , status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
                    return Response({"message": "An Error Occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)