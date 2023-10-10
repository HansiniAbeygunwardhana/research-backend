from django.contrib import admin
from .models  import Meal , keyword , ingredient

# Register your models here.
admin.site.register(Meal)
admin.site.register(keyword)
admin.site.register(ingredient)

