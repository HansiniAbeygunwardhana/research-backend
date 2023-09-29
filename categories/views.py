from django.shortcuts import render
from .models import Category
from rest_framework import viewsets , status 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategorySerializer
# Create your views here.

class CategoryViewSet(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED) 
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request , pk=None):
        if pk:
            categories = Category.objects.get(id=pk)
            if categories:
                serializer = CategorySerializer(categories)
                return Response(serializer.data)
            else:
                return Response({"message":"Category not found"} , status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
    
    def put(self, request, pk):
        categories = Category.objects.get(id=pk)
        serializer = CategorySerializer(categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        categories = Category.objects.get(id=pk)
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)