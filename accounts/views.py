from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
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
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # If the user does not have a profile, redirect to profile creation page
                return redirect('profile_create')

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
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # --- Auto-Calculate BMR & TDEE ---
            if profile.current_weight and profile.height and profile.date_of_birth and profile.gender:
                try:
                    import datetime
                    today = datetime.date.today()
                    age = today.year - profile.date_of_birth.year - ((today.month, today.day) < (profile.date_of_birth.month, profile.date_of_birth.day))
                    
                    # Mifflin-St Jeor Equation
                    bmr = (10 * profile.current_weight) + (6.25 * profile.height) - (5 * age)
                    
                    if profile.gender == 'M':
                        bmr += 5
                    else:
                        bmr -= 161
                    
                    # TDEE
                    activity_multiplier = float(profile.activity_level)
                    tdee = bmr * activity_multiplier
                    
                    profile.calculated_bmr = int(bmr)
                    profile.calculated_tdee = int(tdee)
                    
                    # Auto-set daily goal if not set by user (or strictly for guidance)
                    # For now, let's just save the calculated values so we can show them
                    # Or we can auto-update the goal if the user didn't manually type one?
                    # Let's overwrite safely if it matches the default 2000
                    if profile.daily_calorie_goal == 2000:
                         profile.daily_calorie_goal = int(tdee)

                except Exception as e:
                    print(f"Error calculating BMR: {e}")
            
            profile.save()
            messages.success(request, "Your profile and custom plan have been updated!")
            return redirect('profile')
        else:
            print(form.errors)
            messages.error(request, "There was an error updating your profile.")
    else:
        form = UserProfileForm(instance=profile)

    # --- Generate Custom Plan ---
    # Simple logic: Try to find one meal of each type
    from home.models import Meal
    
    # Defaults
    breakfast = Meal.objects.filter(type__icontains='Breakfast').first()
    lunch = Meal.objects.filter(type__icontains='Lunch').first()
    dinner = Meal.objects.filter(type__icontains='Dinner').first()
    snack = Meal.objects.filter(type__icontains='Snack').first()
    
    custom_plan = [m for m in [breakfast, lunch, dinner, snack] if m]
    
    # Calculate totals
    total_calories = sum(m.calories for m in custom_plan)
    total_protein = sum(m.protein for m in custom_plan)

    context = {
        'form': form, 
        'profile': profile,
        'custom_plan': custom_plan,
        'plan_calories': total_calories,
        'plan_protein': total_protein
    }

    return render(request, 'accounts/profile.html', context)