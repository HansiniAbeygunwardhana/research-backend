from django.db import models
from django.contrib.auth.models import User
from meals.models import Meal

STATUS = (
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed')
)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.meal.name}'

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True , default=100000)
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('meals.Meal', through='OrderItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS, default='confirmed')
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user} - {self.createdAt}'
    