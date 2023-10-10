from django.urls import path
from users.views import JWTLoginView , RegisterView , LogoutView , ResetPasswordView

urlpatterns = [
    path('login/', JWTLoginView.as_view() , name="login"),
    path('register/', RegisterView.as_view() , name="register"),
    path('logout/', LogoutView.as_view() , name="logout"),
    path('reset-password/', ResetPasswordView.as_view() , name="reset-password"),
]
