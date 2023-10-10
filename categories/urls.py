from django.urls import path
from .views import CategoryViewSet

urlpatterns = [
    path('', CategoryViewSet.as_view() , name='categories'),
    path('<int:pk>', CategoryViewSet.as_view() , name='categoriesbyid'),
]
