import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from surprise import Dataset, Reader, SVD


def get_recommendations(user_id, user_ingredients, meal_data, order_data):
            recommended_meals = []
            healthy_meals = []
            based_on_previous_orders = []
    
            order_data = pd.merge(order_data, meal_data, left_on='RecipeId', right_on='RecipeId')
            print(order_data.columns)
            reader = Reader(rating_scale=(1, 5))
            data = Dataset.load_from_df(order_data[['CustomerName', 'Name', 'Rating']], reader)
            

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
            model_filename = "historic-data-aware-model.pkl"
            svd = joblib.load(model_filename)
            print("Loading Model", model_filename)

            # Taking user inputs

            # Processing user inputs
            user_vector = vectorizer.transform([', '.join(user_ingredients)])
            distances, indices = knn.kneighbors(user_vector)

            # Display recommendations
            print("Recommended Meals:")
            print("=================")
            for idx in indices[0]:
                print("- " + meal_data.loc[idx, 'Name'])
                recommended_meals.append(meal_data.loc[idx, 'Name'])

            meals_already_ordered = order_data[order_data['CustomerName'] == user_id]['Name'].unique()
            
            # Get meals that the user has not ordered yet
            all_meals = order_data['Name'].unique()
            meals_to_recommend = [meal for meal in all_meals if meal not in meals_already_ordered]
            
            recommendations = []
            for meal_name in meals_to_recommend:
                prediction = svd.predict(user_id, meal_name)
                recommendations.append((meal_name, prediction.est))

            recommendations.sort(key=lambda x: x[1], reverse=True)

            dataset=meal_data.copy()
            columns=['RecipeId','Name','CookTime','PrepTime','TotalTime','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent','RecipeInstructions']
            dataset=dataset[columns]

            max_Calories=2000
            max_daily_fat=100
            max_daily_Saturatedfat=13
            max_daily_Cholesterol=300
            max_daily_Sodium=2300
            max_daily_Carbohydrate=325
            max_daily_Fiber=40
            max_daily_Sugar=40
            max_daily_Protein=200
            max_list=[max_Calories,max_daily_fat,max_daily_Saturatedfat,max_daily_Cholesterol,max_daily_Sodium,max_daily_Carbohydrate,max_daily_Fiber,max_daily_Sugar,max_daily_Protein]

            extracted_data=dataset.copy()
            for column,maximum in zip(extracted_data.columns[6:15],max_list):
                extracted_data=extracted_data[extracted_data[column]<maximum]

            extracted_data.iloc[:,6:15].corr()

            from sklearn.preprocessing import StandardScaler
            scaler=StandardScaler()
            prep_data=scaler.fit_transform(extracted_data.iloc[:,6:15].to_numpy())

            from sklearn.neighbors import NearestNeighbors
            knn = NearestNeighbors(metric='cosine',algorithm='brute')
            knn.fit(prep_data)

            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import FunctionTransformer
            transformer = FunctionTransformer(knn.kneighbors,kw_args={'return_distance':False})
            pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])

            params={'n_neighbors':10,'return_distance':False}
            pipeline.get_params()
            pipeline.set_params(NN__kw_args=params)

            pipeline.transform(extracted_data.iloc[0:1,6:15].to_numpy())[0]

            extracted_data[extracted_data['RecipeIngredientParts'].str.contains("",regex=False)]

            ingredient_db = set()
            for ingredients in extracted_data['RecipeIngredientParts']:
                ingredient_list = ingredients.split(',')
                ingredient_db.update([ingredient.strip() for ingredient in ingredient_list])

            vectorizer = TfidfVectorizer()
            meal_vectors = vectorizer.fit_transform(extracted_data['RecipeIngredientParts'].values)

            n_neighbors = 5  # Number of nearest neighbors to consider
            knn2 = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
            knn2.fit(meal_vectors)


            user_vector = vectorizer.transform([', '.join(user_ingredients)])
            distances, indices = knn2.kneighbors(user_vector)

            print("Hey! You better to try below healthy meals:")
            print("=======================================")
            for idx in indices[0]:
                healthy_meals.append(dataset.loc[idx, 'Name'])
                print("- " + dataset.loc[idx, 'Name'])
            print("")

            if user_id == 0:
                print ("place your order below")

            else:
                print("Based on your previous orders")
                print("=============================")
                for meal_name, rating in recommendations[:5]:
                    based_on_previous_orders.append(meal_name)
                    print("- " + f"{meal_name}")
            print("")
    
    
    
            return recommended_meals, healthy_meals, based_on_previous_orders