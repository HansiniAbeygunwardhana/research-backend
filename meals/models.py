from django.db import models

class keyword(models.Model):
    keyword = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.keyword
    
class ingredient(models.Model):
    ingredient = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.ingredient

# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=100, null=False , unique=True)
    description = models.TextField(null=False)
    calories = models.FloatField(null=False , default=0)
    carbohydrateContent = models.FloatField(null=False , default=0)
    cholesterolContent = models.FloatField(null=False , default=0)
    fatContent = models.FloatField(null=False , default=0)
    fiberContent = models.FloatField(null=False , default=0)
    proteinContent = models.FloatField(null=False , default=0)
    saturatedFatContent = models.FloatField(null=False , default=0)
    sodiumContent = models.FloatField(null=False , default=0)
    sugarContent = models.FloatField(null=False , default=0)
    image = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False , default=0)
    keywords = models.ManyToManyField(keyword , related_name='keywords')
    ingredients = models.ManyToManyField(ingredient , related_name='ingredients')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    
    