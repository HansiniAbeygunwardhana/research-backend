
from django.contrib import admin
from django.urls import path , include
from rest_framework import routers


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("cat/", include("categories.urls")),
    path("meals/", include("meals.urls")),
    path("auth/", include("users.urls")),
    path("search/", include("recommandation.urls")),
    path("health/" , include("healthprofiles.urls")),
    path("order/" , include("orders.urls"))
]
