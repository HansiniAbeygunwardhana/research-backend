from django.db import models , transaction
from cloudinary.models import CloudinaryField
from recommandation.models import Recipe
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # Save the Meal instance first to generate an ID
            super(Meal, self).save(*args, **kwargs)

            # Wrap the count printing in a transaction
            transaction.on_commit(self.save_recepie)

    def save_recepie(self):
        keywords_list = []
        ingredients_list = []  
        keywords_string = ''
        ingredients_string = ''
        for keyword in self.keywords.all():
            keywords_list.append('"' + keyword.keyword + '"')
        for ingredient in self.ingredients.all():
            ingredients_list.append('"' + ingredient.ingredient + '"')
            
        keywords_string = ', '.join(keywords_list)
        ingredients_string = ', '.join(ingredients_list)
            
            # Now create and save the Recipe object
        recipe = Recipe(
            Name=self.name,
            Description=self.description,
            Calories=self.calories,
            FatContent=self.fatContent,
            SaturatedFatContent=self.saturatedFatContent,
            CholesterolContent=self.cholesterolContent,
            SodiumContent=self.sodiumContent,
            CarbohydrateContent=self.carbohydrateContent,
            FiberContent=self.fiberContent,
            SugarContent=self.sugarContent,
            ProteinContent=self.proteinContent,
            Keywords = "c(" + keywords_string +  ")",
            RecipeIngredientParts = "c(" + ingredients_string +  ")",
        )
        recipe.save()
        
        print('Number of keywords:', keywords_string)
        print('Number of ingredients:', ingredients_string)