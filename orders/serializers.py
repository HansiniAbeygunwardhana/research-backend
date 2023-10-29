from rest_framework import serializers
from .models import Order , OrderItem
from meals.models import Meal  # Import Meal model
from django.contrib.auth.models import User  # Import User model

        
class ItemsOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = ['id' , 'quantity']
        
class OrderBasicSerializer(serializers.ModelSerializer):\
    
    class Meta:
        model = Order
        fields = ['id' , 'createdAt' , 'total'  , 'status']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'email')
        
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ( 'name', 'price')
        

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.DecimalField(source='meal.price', read_only=True , max_digits=10, decimal_places=2)
    image_1 = serializers.ImageField(source='meal.image_1', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('name', 'price', 'quantity' , 'image_1')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True  , source='orderitem_set')  # Use the OrderItemSerializer to serialize related items
    user = UserSerializer()  # Use the UserSerializer to serialize related users

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'total', 'status',  'user', 'items')