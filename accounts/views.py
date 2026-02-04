from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate that all fields are filled out
        if not username or not email or not password1 or not password2:
            messages.error(request, "Please fill out all fields.")
            return redirect('register')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Create the user profile after saving the user
            UserProfile.objects.create(user=user)

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Something went wrong: {e}. Please try again.")
            return redirect('register')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in

            # Check if the user has a profile
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # If the user does not have a profile, redirect to profile page to create one
                return redirect('profile')

            # Successful login
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')  # Redirect to the user's profile page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    try:
        # Try to fetch the existing user profile
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If no profile exists, create a new one
        profile = None

    # Handle the form submission (to create or update the profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the profile, ensuring it's associated with the current user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')  # Redirect to the same page after saving changes
    else:
        # If it's a GET request, load the profile form with the user's profile (if exists)
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})