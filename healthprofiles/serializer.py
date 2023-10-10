from rest_framework import serializers
from .models import HealthProfile

class HealthProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HealthProfile
        fields = ['calories' , 'carbohydrateContent' , 'cholesterolContent' , 'fatContent' , 'fiberContent' , 'proteinContent' , 'saturatedFatContent' , 'sodiumContent' , 'sugarContent' , 'condition_name' ]
