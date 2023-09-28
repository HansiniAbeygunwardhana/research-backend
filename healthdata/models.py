from django.db import models

# Create your models here.
class healthdata(models.Model):
    calories = models.FloatField(null=False),
    carbohydrateContent = models.FloatField(null=False),
    cholesterolContent = models.FloatField(null=False),
    fatContent = models.FloatField(null=False),
    fiberContent = models.FloatField(null=False),
    proteinContent = models.FloatField(null=False),
    saturatedFatContent = models.FloatField(null=False),
    sodiumContent = models.FloatField(null=False),
    sugarContent = models.FloatField(null=False),
    condition_name = models.CharField(max_length=100, null=False),
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.condition_name