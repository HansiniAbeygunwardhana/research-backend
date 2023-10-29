from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from meals.models import keyword, Meal
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from surprise import Dataset, Reader, SVD
import mysql.connector
from .models import Review, Recipe, UserProfile
from .utils import get_recommendations
from meals.models import Meal
from meals.serializers import MealSerializerBasic

# Here Lies the machine learning model

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="research_db"
)


class RecommandationView(APIView):
    
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request : HttpRequest):
        meal_type = request.GET.getlist('meal' , [])
        meal_type = [meal.lower() for meal in meal_type]
        print(meal_type)
        recommended_meals = []
        healthy_meals = []
        based_on_previous_orders = []
        recommended_meals_obj = []
        healthy_meals_obj = []
        based_on_previous_orders_obj = []
        
        if conn.is_connected():
            print('Connected to MySQL database')

            # Load meal data from MySQL
            meal_data = pd.read_sql('SELECT * FROM recommandation_recipe', conn)
            meal_data['RecipeIngredientParts'] = meal_data['RecipeIngredientParts'].str.lower()
            reader = Reader(rating_scale=(1, 5))
            order_data = pd.read_sql('SELECT * FROM recommandation_review', conn)
            
            user_id = 2008
            user_ingredients = meal_type
            recommended_meals, healthy_meals, based_on_previous_orders = get_recommendations(user_id, user_ingredients, meal_data, order_data)
            
            for meal_name in recommended_meals:
                try:
                    meal = Meal.objects.get(name=meal_name)
                    recommended_meals_obj.append(MealSerializerBasic(meal).data)
                except Meal.DoesNotExist:
                    pass
            
            for meal_name in healthy_meals:
                try:
                    meal = Meal.objects.get(name=meal_name)
                    healthy_meals_obj.append((MealSerializerBasic(meal).data))
                except Meal.DoesNotExist:
                    pass
                
            for meal_name in based_on_previous_orders:
                try:
                    meal = Meal.objects.get(name=meal_name)
                    based_on_previous_orders_obj.append((MealSerializerBasic(meal).data))
                except Meal.DoesNotExist:
                    pass 
            
            responseData = {
                'message' : 'Recommandation Successful',
                'recommended_meals' : recommended_meals_obj,
                'healthy_meals' : healthy_meals_obj,
                'based_on_previous_orders' : based_on_previous_orders_obj
            }
            
            return Response(responseData , status=status.HTTP_200_OK) 
        else:
            print('Connection to MySQL database failed')
            
            responseData = {
                'message' : 'Recommandation Failed',
                'entered meals' : meal_type
            }
            
            return Response(responseData , status=status.HTTP_400_BAD_REQUEST)
  
  
          
            
        
        
    
        