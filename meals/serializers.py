from rest_framework import serializers
from .models import Meal , keyword , ingredient

class keywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = keyword
        fields = '__all__'
        
class ingredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredient
        fields = '__all__'
        
class MealSerializer(serializers.ModelSerializer):
    keywords = keywordSerializer(many=True)
    ingredients = ingredientSerializer(many=True)
    
    class Meta:
        model = Meal
        fields = '__all__'
        
    def create(self , validated_data):
        keywords_data = validated_data.pop('keywords')
        ingredients_data = validated_data.pop('ingredients')
        meal = Meal.objects.create(**validated_data)
        for keyword_data in keywords_data:
            keyword_obj , create = keyword.objects.get_or_create(keyword=keyword_data['keyword'])
            meal.keywords.add(keyword_obj)
        for ingredient_data in ingredients_data:
            ingredient_obj , create = ingredient.objects.get_or_create(ingredient=ingredient_data['ingredient'])
            meal.ingredients.add(ingredient_obj)
        return meal
    