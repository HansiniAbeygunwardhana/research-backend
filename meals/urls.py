from django.urls import path
from .views import MealView

urlpatterns = [
    path('' , MealView.as_view() , name='meal'),
]
