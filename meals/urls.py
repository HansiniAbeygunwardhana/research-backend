from django.urls import path
from .views import MealView , KeywordView

urlpatterns = [
    path('' , MealView.as_view() , name='meal'),
    path('<int:pk>' , MealView.as_view() , name='meal'),
    path('keywords' , KeywordView.as_view() , name="Keywords")
]
