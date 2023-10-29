from django.db import models
from cloudinary.models import CloudinaryField

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
    price = models.FloatField(null=False , default=0)
    keywords = models.ManyToManyField(keyword , related_name='keywords')
    ingredients = models.ManyToManyField(ingredient , related_name='ingredients')
    created_at = models.DateTimeField(auto_now_add=True)
    image_1 = CloudinaryField('Image 1', null=True, blank=True)
    image_2 = CloudinaryField('Image 2', null=True, blank=True)
    image_3 = CloudinaryField('Image 3', null=True, blank=True)
    image_4 = CloudinaryField('Image 4', null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    
    