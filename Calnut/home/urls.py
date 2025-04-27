from django.contrib import admin
from django.urls import path 
from home import views


admin.site.site_header = "Calnut Admin"
admin.site.site_title = "Calnut Admin Portal"
admin.site.index_title = "Welcome to Calnut-Nutrition Tracker"

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('about', views.about , name='about'),
    path('blogs', views.blogs , name='blogs'),
    path('food', views.food , name='food'),
    path('nutrition', views.nutrition , name='nutrition'),
    path('track', views.calories, name='calories'),
    path('graphs', views.graphs, name='graphs'),
    path('meals', views.meals, name='meals'),
    path('food', views.food, name='food'),
    path('recipes', views.recipes, name='recipes'),
    path('blogs', views.blogs, name='blogs'),
    
]
