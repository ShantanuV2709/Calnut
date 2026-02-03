from django.contrib import admin
from .models import FoodItem, Meal, UserFoodLog

admin.site.register(FoodItem)
admin.site.register(Meal)
admin.site.register(UserFoodLog)
