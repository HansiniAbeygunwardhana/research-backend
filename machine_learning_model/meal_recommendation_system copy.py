# # Meal Recommendation System - Ingredients Aware
# ## Scope of the code
# - Focusing on using already built recommendation model to generate recommendation

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector

#### Importing data

meal_data=pd.read_csv("test.csv")
meal_data['RecipeIngredientParts'] = meal_data['RecipeIngredientParts'].str.lower()

### Preparing database
ingredient_db = set()
for ingredients in meal_data['RecipeIngredientParts']:
    ingredient_list = ingredients.split(',')
    ingredient_db.update([ingredient.strip() for ingredient in ingredient_list])

##### Converting data in to feature vectors
vectorizer = TfidfVectorizer()
meal_vectors = vectorizer.fit_transform(meal_data['RecipeIngredientParts'].values)

## Importing the recommendation model
import joblib
model_filename = "ingredients-aware-model.pkl"
knn = joblib.load(model_filename)
print("Loading Model", model_filename)

# Taking user inputs
user_input = input("Enter your prefered ingredients (comma-separated): ")
user_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(",")]

# Processing user inputs
user_vector = vectorizer.transform([', '.join(user_ingredients)])
distances, indices = knn.kneighbors(user_vector)

### Display recommendations
print("Recommended Meals:")
for idx in indices[0]:
    print(meal_data.loc[idx, 'Name'])
