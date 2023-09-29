from django.urls import path
from .views import HealthProfileView

urlpatterns = [
    path('' , HealthProfileView.as_view() , name='healthprofiles'),
    path('<int:pk>/' , HealthProfileView.as_view() , name='healthprofilesbyid'),
]
