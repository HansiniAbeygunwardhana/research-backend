# # Meal Recommendation System - Ingredients Aware
# ## Scope of the code
# - Focusing on using already built recommendation model to generate recommendation

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector
import joblib


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sample_data"
)

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
    user_input = input("Enter your preferred ingredients (comma-separated): ")
    user_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(",")]

    # Processing user inputs
    user_vector = vectorizer.transform([', '.join(user_ingredients)])
    distances, indices = knn.kneighbors(user_vector)

    # Display recommendations
    print("Recommended Meals:")
    for idx in indices[0]:
        print(meal_data.loc[idx, 'Name'])

    # Close the MySQL connection
    conn.close()
else:
    print('Connection to MySQL database failed')
