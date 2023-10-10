from rest_framework import serializers
from .models import Meal , keyword , ingredient

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = keyword
        fields = '__all__'
        
class KeywordSerialiserBasic(serializers.ModelSerializer):
    
    
    class Meta :
        model = keyword
        fields = ['keyword']
        
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredient
        fields = '__all__'
        
class MealSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(child=serializers.CharField())
    ingredients = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Meal
        fields = '__all__'

    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords')
        ingredients_data = validated_data.pop('ingredients')
        meal = Meal.objects.create(**validated_data)

        for keyword_data in keywords_data:
            keyword_obj, created = keyword.objects.get_or_create(keyword=keyword_data)
            meal.keywords.add(keyword_obj)

        for ingredient_data in ingredients_data:
            ingredient_obj, created = ingredient.objects.get_or_create(ingredient=ingredient_data)
            meal.ingredients.add(ingredient_obj)
            
        return meal
    

    
class MealSerializerBasic(serializers.ModelSerializer):
    
    ingredients = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    
    class Meta:
        model = Meal
        fields = ['id' , 'name' , 'description' ,'image' , 'price' , 'ingredients' , 'keywords']
        
    def get_ingredients(self, obj):
        return [ingredient.ingredient for ingredient in obj.ingredients.all()]
    def get_keywords(self, obj):
        return [keyword.keyword for keyword in obj.keywords.all()]
    
class MealSerializerExtended(MealSerializerBasic):
    
    class Meta:
        model = Meal
        fields = '__all__'
        

    