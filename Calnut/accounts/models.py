# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)  # Add location field
    date_of_birth = models.DateField(null=True, blank=True)  # Add date_of_birth field
    bio = models.TextField(blank=True, null=True)  # Add bio field (a TextField for long text)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Add profile picture field

    def __str__(self):
        return self.user.username
