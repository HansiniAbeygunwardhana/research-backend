from django.urls import path
from .views import OrderCreateView , OrderView , LastOrderView

urlpatterns = [
    path('' , OrderCreateView.as_view() ,  name='order'),
    path('<int:pk>/' , OrderView.as_view() , name='order'),
    path('list' , OrderView.as_view() , name='order'),
    path('last' , LastOrderView.as_view() , name='order'),
]
