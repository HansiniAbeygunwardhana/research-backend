from rest_framework import serializers
from .models import HealthProfile
from recommandation.models import UserProfile

class HealthProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HealthProfile
        fields = ['calories' , 'carbohydrateContent' , 'cholesterolContent' , 'fatContent' , 'fiberContent' , 'proteinContent' , 'saturatedFatContent' , 'sodiumContent' , 'sugarContent' , 'condition_name' ]



class UserProfileAndHealthProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='userprofile.user')
    fav_ing_1 = serializers.CharField(max_length=11, source='userprofile.fav_ing_1')
    fav_ing_2 = serializers.CharField(max_length=11, allow_blank=True, allow_null=True, source='userprofile.fav_ing_2')
    fav_ing_3 = serializers.CharField(max_length=11, allow_blank=True, allow_null=True, source='userprofile.fav_ing_3')
    health_condition_1 = serializers.CharField(max_length=41, allow_blank=True, allow_null=True, source='userprofile.health_condition_1')
    health_condition_2 = serializers.CharField(max_length=41, allow_blank=True, allow_null=True, source='userprofile.health_condition_2')
    health_condition_3 = serializers.CharField(max_length=41, allow_blank=True, allow_null=True, source='userprofile.health_condition_3')
    prefered_diet_category = serializers.CharField(max_length=13, allow_blank=True, allow_null=True, source='userprofile.prefered_diet_category')
    calories = serializers.FloatField(allow_null=True, source='healthprofile.calories')
    carbohydrateContent = serializers.FloatField(allow_null=True, source='healthprofile.carbohydrateContent')
    cholesterolContent = serializers.FloatField(allow_null=True, source='healthprofile.cholesterolContent')
    fatContent = serializers.FloatField(allow_null=True, source='healthprofile.fatContent')
    fiberContent = serializers.FloatField(allow_null=True, source='healthprofile.fiberContent')
    proteinContent = serializers.FloatField(allow_null=True, source='healthprofile.proteinContent')
    saturatedFatContent = serializers.FloatField(allow_null=True, source='healthprofile.saturatedFatContent')
    sodiumContent = serializers.FloatField(allow_null=True, source='healthprofile.sodiumContent')
    sugarContent = serializers.FloatField(allow_null=True, source='healthprofile.sugarContent')
    condition_name = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, source='healthprofile.condition_name')

    class Meta:
        model = HealthProfile
        fields = [
            'user', 'fav_ing_1', 'fav_ing_2', 'fav_ing_3',
            'health_condition_1', 'health_condition_2', 'health_condition_3',
            'prefered_diet_category', 'calories', 'carbohydrateContent',
            'cholesterolContent', 'fatContent', 'fiberContent', 'proteinContent',
            'saturatedFatContent', 'sodiumContent', 'sugarContent', 'condition_name'
        ]
