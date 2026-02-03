"""
URL configuration for Calnut project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views from individual apps
from home import views as home_views
from accounts import views as accounts_views

# Admin Site Config
admin.site.site_header = "Calnut Admin"
admin.site.site_title = "Calnut Admin Portal"
admin.site.index_title = "Welcome to Calnut-Nutrition Tracker"

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home Integration
    path('', home_views.home, name='home'),
    path('calories/', home_views.calories, name='calories'),
    path('meals/', home_views.meals, name='meals'),
    path('food/', home_views.food, name='food'),
    path('diary/', home_views.diary, name='diary'),
    path('add_food_log/', home_views.add_food_log, name='add_food_log'),
    path('add_water/', home_views.add_water, name='add_water'),
    path('analytics/', home_views.analytics, name='analytics'),
    path('add_exercise/', home_views.add_exercise, name='add_exercise'),
    path('export/csv/', home_views.export_csv, name='export_csv'),
    path('export/pdf/', home_views.export_pdf, name='export_pdf'),
    # Accounts Integration
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('accounts/register/', accounts_views.register_view, name='register'),
    path('accounts/logout/', accounts_views.logout_view, name='logout'),
    path('accounts/profile/', accounts_views.profile_view, name='profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
