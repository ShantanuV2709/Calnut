from django.contrib import admin
from .models import FoodItem, Meal, UserFoodLog, WaterLog, ExerciseLog

admin.site.register(FoodItem)
admin.site.register(Meal)
admin.site.register(UserFoodLog)
admin.site.register(WaterLog)
admin.site.register(ExerciseLog)
