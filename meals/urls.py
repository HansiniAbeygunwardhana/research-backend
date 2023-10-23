from django.urls import path
from .views import MealView , KeywordView , MealListView

urlpatterns = [
    path('' , MealView.as_view() , name='meal'),
    path('<int:pk>' , MealView.as_view() , name='meal'),
    path('keywords' , KeywordView.as_view() , name="Keywords"),
    path('list' , MealListView.as_view() , name="Meal List"),
]
