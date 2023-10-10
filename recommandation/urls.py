from django.urls import path
from .views import RecommandationView

urlpatterns = [
    path('', RecommandationView.as_view()),
]
