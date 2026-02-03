from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + UserProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500'})
    )
    activity_level = forms.ChoiceField(
        choices=[('', 'Select Activity Level')] + UserProfile.ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500'})
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'location', 'date_of_birth', 'gender', 'height', 'current_weight', 'goal_weight', 'activity_level', 'daily_calorie_goal']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where are you located?'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'height': forms.NumberInput(attrs={'placeholder': 'Height (cm)'}),
            'current_weight': forms.NumberInput(attrs={'placeholder': 'Current Weight (kg)'}),
            'goal_weight': forms.NumberInput(attrs={'placeholder': 'Goal Weight (kg)'}),
            'daily_calorie_goal': forms.NumberInput(attrs={'placeholder': 'Daily Calculator Target (Auto-filled if info provided)'}),
        }
