from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from recommandation.models import UserProfile

# Create your models here.
class HealthProfile(models.Model):
    calories = models.FloatField(null=False , default=0)
    carbohydrateContent = models.FloatField(null=False , default=0)
    cholesterolContent = models.FloatField(null=False , default=0)
    fatContent = models.FloatField(null=False , default=0)
    fiberContent = models.FloatField(null=False , default=0)
    proteinContent = models.FloatField(null=False , default=0)
    saturatedFatContent = models.FloatField(null=False , default=0)
    sodiumContent = models.FloatField(null=False , default=0)
    sugarContent = models.FloatField(null=False , default=0)
    condition_name = models.CharField(max_length=100, null=False , default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.condition_name
    