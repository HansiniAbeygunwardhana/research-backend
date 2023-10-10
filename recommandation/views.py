from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from meals.models import keyword
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import mysql.connector

# Here Lies the machine learning model

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sample_data"
)


class RecommandationView(APIView):
    
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request : HttpRequest):
        meal_type = request.GET.getlist('meal' , [])
        meal_type = [meal.lower() for meal in meal_type]
        print(meal_type)
        recommended_meals = []
        
        if conn.is_connected():
            print('Connected to MySQL database')

            # Load meal data from MySQL
            meal_data = pd.read_sql('SELECT * FROM mytable', conn)
            meal_data['RecipeIngredientParts'] = meal_data['RecipeIngredientParts'].str.lower()

            # Prepare database
            ingredient_db = set()
            for ingredients in meal_data['RecipeIngredientParts']:
                ingredient_list = ingredients.split(',')
                ingredient_db.update([ingredient.strip() for ingredient in ingredient_list])

            # Convert data into feature vectors
            vectorizer = TfidfVectorizer()
            meal_vectors = vectorizer.fit_transform(meal_data['RecipeIngredientParts'].values)

            # Load the recommendation model
            model_filename = "ingredients-aware-model.pkl"
            knn = joblib.load(model_filename)
            print("Loading Model", model_filename)

            # Taking user inputs
            user_ingredients = meal_type

            # Processing user inputs
            user_vector = vectorizer.transform([', '.join(user_ingredients)])
            distances, indices = knn.kneighbors(user_vector)

            # Display recommendations
            print("Recommended Meals:")
            for idx in indices[0]:
                recommended_meals.append(meal_data.loc[idx, 'Name'])

            
            responseData = {
                'message' : 'Recommandation Successfull',
                'meals' : recommended_meals
            }
            
            return Response(responseData , status=status.HTTP_200_OK) 
        else:
            print('Connection to MySQL database failed')
            
            responseData = {
                'message' : 'Recommandation Failed',
                'entered meals' : meal_type
            }
            
            return Response(responseData , status=status.HTTP_400_BAD_REQUEST)
            
            
        
        
    
        