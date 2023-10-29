from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import Order , OrderItem
from .serializers import OrderSerializer , ItemsOrderSerializer ,  OrderBasicSerializer
from meals.models import Meal
# Create your views here.

class OrderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = ItemsOrderSerializer(data=data, many=True)

        if serializer.is_valid():
            # Create an Order instance for the user
            order = Order.objects.create(
                user=user,
                total=0.00  # Initialize total to 0
            )

            for item in serializer.validated_data:
                meal_id = item['id']
                quantity = item['quantity']

                try:
                    meal = Meal.objects.get(pk=meal_id)
                except Meal.DoesNotExist:
                    return Response({'message': f'Meal with ID {meal_id} not found'}, status=status.HTTP_400_BAD_REQUEST)

                total_price = meal.price * quantity

                # Create an OrderItem to associate the meal with the order and store the quantity
                OrderItem.objects.create(order=order, meal=meal, quantity=quantity)

                # Update the total price of the order
                order.total += total_price
                order.save()

            return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

              
class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self , request , pk=None):
        user = request.user
        print(user)
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'message': f'Order with ID {pk} not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            orders = Order.objects.filter(user=user)
            serializer = OrderBasicSerializer(orders , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        
class LastOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self , request):
        user = request.user
        try:
            latest_order = Order.objects.filter(user=user).latest('createdAt')
            serializer = OrderSerializer(latest_order)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': f'not found'}, status=status.HTTP_400_BAD_REQUEST)
                
                
            
            
        


