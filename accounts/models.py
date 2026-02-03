# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)  # Add location field
    date_of_birth = models.DateField(null=True, blank=True)  # Add date_of_birth field
    bio = models.TextField(blank=True, null=True)  # Add bio field (a TextField for long text)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Add profile picture field
    
    # [NEW] Goals & Stats
    # [NEW] Goals & Stats
    current_weight = models.FloatField(blank=True, null=True)
    goal_weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)  # cm
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    ACTIVITY_CHOICES = [
        ('1.2', 'Sedentary (little or no exercise)'),
        ('1.375', 'Lightly active (light exercise 1-3 days/week)'),
        ('1.55', 'Moderately active (moderate exercise 3-5 days/week)'),
        ('1.725', 'Very active (hard exercise 6-7 days/week)'),
        ('1.9', 'Extra active (very hard exercise & physical job)'),
    ]
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, default='1.2')
    
    daily_calorie_goal = models.IntegerField(default=2000)
    calculated_bmr = models.IntegerField(blank=True, null=True)
    calculated_tdee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
