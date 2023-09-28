from django.db import models


class keyword(models.Model):
    keyword = models.CharField(max_length=100, null=False),
    created_at = models.DateTimeField(auto_now_add=True)
    
class ingredient(models.Model):
    ingredient = models.CharField(max_length=100, null=False),
    created_at = models.DateTimeField(auto_now_add=True)

class mealdata(models.Model):
    calories = models.FloatField(null=False),
    carbohydrateContent = models.FloatField(null=False),
    cholesterolContent = models.FloatField(null=False),
    fatContent = models.FloatField(null=False),
    fiberContent = models.FloatField(null=False),
    proteinContent = models.FloatField(null=False),
    saturatedFatContent = models.FloatField(null=False),
    sodiumContent = models.FloatField(null=False),
    sugarContent = models.FloatField(null=False),
    title = models.CharField(max_length=100, null=False),
    description = models.CharField(max_length=100, null=False),
    image = models.CharField(max_length=100, null=False),
    price = models.FloatField(null=False),
    keywords = models.ManyToManyField(keyword),
    ingredients = models.ManyToManyField(ingredient),
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.title
    
