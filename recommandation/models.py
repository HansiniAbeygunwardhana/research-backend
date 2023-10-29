from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(max_length=22)
    fav_ing_1 = models.CharField(max_length=11)
    fav_ing_2 = models.CharField(max_length=11, blank=True, null=True)
    fav_ing_3 = models.CharField(max_length=11, blank=True, null=True)
    health_condition_1 = models.CharField(max_length=41, blank=True, null=True)
    health_condition_2 = models.CharField(max_length=41, blank=True, null=True)
    health_condition_3 = models.CharField(max_length=41, blank=True, null=True)
    prefered_diet_category = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        self.user_name = self.user.username
        super(UserProfile, self).save(*args, **kwargs)
    
    
class Review(models.Model):
    ReviewId = models.IntegerField(primary_key=True)
    RecipeId = models.IntegerField()
    CustomerID = models.IntegerField()
    CustomerName = models.CharField(max_length=19)
    Rating = models.IntegerField()
    Review = models.CharField(max_length=857)
    DateSubmitted = models.CharField(max_length=20)
    DateModified = models.CharField(max_length=20)

    def __str__(self):
        return f"Review by {self.CustomerName} for Recipe {self.RecipeId}"
    
class Recipe(models.Model):
    RecipeId = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=65)
    AuthorId = models.IntegerField()
    AuthorName = models.CharField(max_length=20)
    CookTime = models.CharField(max_length=9)
    PrepTime = models.CharField(max_length=8)
    TotalTime = models.CharField(max_length=11)
    DatePublished = models.CharField(max_length=20)
    Description = models.TextField()
    Images = models.TextField()
    RecipeCategory = models.CharField(max_length=28)
    Keywords = models.TextField()
    RecipeIngredientQuantities = models.TextField()
    RecipeIngredientParts = models.TextField()
    AggregatedRating = models.CharField(max_length=3)
    ReviewCount = models.CharField(max_length=3)
    Calories = models.DecimalField(max_digits=7, decimal_places=1)
    FatContent = models.DecimalField(max_digits=6, decimal_places=1)
    SaturatedFatContent = models.DecimalField(max_digits=6, decimal_places=1)
    CholesterolContent = models.DecimalField(max_digits=8, decimal_places=1)
    SodiumContent = models.DecimalField(max_digits=8, decimal_places=1)
    CarbohydrateContent = models.DecimalField(max_digits=6, decimal_places=1)
    FiberContent = models.DecimalField(max_digits=5, decimal_places=1)
    SugarContent = models.DecimalField(max_digits=6, decimal_places=1)
    ProteinContent = models.DecimalField(max_digits=6, decimal_places=1)
    RecipeServings = models.CharField(max_length=4)
    RecipeYield = models.CharField(max_length=51)
    RecipeInstructions = models.TextField()
    
    def __str__(self):
        return f"{self.RecipeId} - {self.Name}"