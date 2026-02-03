from django.shortcuts import render, HttpResponse, redirect
from .models import FoodItem, Meal, UserFoodLog, WaterLog, ExerciseLog
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
import csv
from accounts.models import UserProfile
from .utils import fetch_food_data

def calculate_streak(user):
    """Calculate consecutive days the user has logged food"""
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    streak = 0
    check_date = today
    
    while True:
        # Check if user logged anything on check_date
        start_of_day = datetime.combine(check_date, datetime.min.time())
        end_of_day = datetime.combine(check_date, datetime.max.time())
        start_of_day = timezone.make_aware(start_of_day)
        end_of_day = timezone.make_aware(end_of_day)
        
        logs = UserFoodLog.objects.filter(
            user=user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        ).exists()
        
        if logs:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
            
        # Safety limit to prevent infinite loops
        if streak > 365:
            break
    
    return streak

# Create your views here.
def home(request):
    return render(request,'home.html')

def calories(request):
    return render(request, 'calories.html')

def meals(request):
    # Fetch meals from DB
    meals_list = Meal.objects.all()
    # If no meals, we might want to manually create some or handle empty state
    # For now, let's pass what we have
    return render(request, 'meals.html', {'meals': meals_list})


def food(request):
    query = request.GET.get('q')
    food_items = []
    
    if query:
        # 1. Search DB first
        food_items = list(FoodItem.objects.filter(name__icontains=query))
        
        # 2. If valid results are scarce (< 2), try API
        if len(food_items) < 2:
            print(f"Searching API for: {query}")
            api_results = fetch_food_data(query)
            
            if api_results:
                # Optimized: Batch check for existence
                api_ids = [item['api_id'] for item in api_results if item.get('api_id')]
                existing_api_ids = set(FoodItem.objects.filter(api_id__in=api_ids).values_list('api_id', flat=True))
                
                new_items = []
                for item in api_results:
                    # Only add if not in existing IDs
                    if item.get('api_id') and item['api_id'] not in existing_api_ids:
                        # Double check to prevent duplicates in list
                        if item['api_id'] not in [x.api_id for x in new_items]:
                            new_items.append(FoodItem(
                                name=item['name'],
                                calories=item['calories'],
                                protein=item['protein'],
                                carbs=item['carbs'],
                                fat=item['fat'],
                                fiber=item['fiber'],
                                sugar=item['sugar'],
                                category=item['category'],
                                image=item['image'],
                                api_id=item['api_id']
                            ))
                
                # Bulk create is faster
                if new_items:
                    try:
                        FoodItem.objects.bulk_create(new_items)
                        print(f"Bulk created {len(new_items)} items")
                    except Exception as e:
                        print(f"Bulk create failed, falling back to looop: {e}")
                        for item in new_items:
                             try: item.save() 
                             except: pass
                
                # Re-query DB to show everything (including newly added)
                food_items = FoodItem.objects.filter(name__icontains=query)
            else:
                # [NEW] Notify user if API failed or returned nothing
                from django.contrib import messages
                messages.warning(request, "External search timed out or found nothing. Showing local results.")

    else:
        # Default view: Show recent items (Djongo has issues with order_by('?'))
        food_items = FoodItem.objects.all().order_by('-id')[:20]
    
    return render(request, 'food.html', {'food_items': food_items})


@login_required
def diary(request):
    today = timezone.now().date()
    # Djongo doesn't support __date lookup, use date range instead
    from datetime import datetime, timedelta
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # Make them timezone-aware
    start_of_day = timezone.make_aware(start_of_day)
    end_of_day = timezone.make_aware(end_of_day)
    
    logs = UserFoodLog.objects.filter(
        user=request.user, 
        date_added__gte=start_of_day,
        date_added__lte=end_of_day
    )
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    # Calculate totals
    total_calories = sum(log.food_item.calories * log.quantity for log in logs)
    total_protein = sum(log.food_item.protein * log.quantity for log in logs)
    
    # Group by meal
    meals = {
        'Breakfast': logs.filter(meal_type='Breakfast'),
        'Lunch': logs.filter(meal_type='Lunch'),
        'Dinner': logs.filter(meal_type='Dinner'),
        'Snack': logs.filter(meal_type='Snack'),
    }
    
    # Calculate goal progress
    calorie_goal = profile.daily_calorie_goal if profile else 2000
    calorie_progress = (total_calories / calorie_goal * 100) if calorie_goal > 0 else 0
    
    # Protein goal estimation (rough: 0.8g per kg body weight, or 15% of calories)
    if profile and profile.current_weight:
        protein_goal = profile.current_weight * 0.8  # grams
    else:
        protein_goal = calorie_goal * 0.15 / 4  # 15% of cals, 4 cal/g protein
    
    protein_progress = (total_protein / protein_goal * 100) if protein_goal > 0 else 0
    
    # Calculate water intake
    water_logs = WaterLog.objects.filter(
        user=request.user,
        date_added__gte=start_of_day,
        date_added__lte=end_of_day
    )
    total_water = sum(log.amount_ml for log in water_logs)
    water_goal = 2000  # 2 liters = 2000ml daily recommendation
    water_progress = (total_water / water_goal * 100) if water_goal > 0 else 0
    
    # Calculate logging streak
    streak = calculate_streak(request.user)
    
    # Calculate exercise calories burned
    exercise_logs = ExerciseLog.objects.filter(
        user=request.user,
        date_added__gte=start_of_day,
        date_added__lte=end_of_day
    )
    total_exercise_calories = sum(log.calories_burned for log in exercise_logs)
    
    # Net calories = consumed - burned
    net_calories = total_calories - total_exercise_calories
    
    context = {
        'logs': logs,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'calorie_goal': calorie_goal,
        'protein_goal': protein_goal,
        'calorie_progress': calorie_progress,
        'protein_progress': protein_progress,
        'total_water': total_water,
        'water_goal': water_goal,
        'water_progress': water_progress,
        'streak': streak,
        'exercise_logs': exercise_logs,
        'total_exercise_calories': total_exercise_calories,
        'net_calories': net_calories,
        'meals': meals,
        'profile': profile
    }
    return render(request, 'diary.html', context)

@login_required
def add_food_log(request):
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        meal_type = request.POST.get('meal_type')
        quantity = float(request.POST.get('quantity', 1))
        photo = request.FILES.get('photo')  # Get uploaded photo
        
        food = FoodItem.objects.get(id=food_id)
        UserFoodLog.objects.create(
            user=request.user,
            food_item=food,
            meal_type=meal_type,
            quantity=quantity,
            photo=photo
        )
        return redirect('diary')
    return redirect('food')

@login_required
def analytics(request):
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    labels = []
    calories_data = []
    protein_data = []
    water_data = []
    
    # Gather data for past 7 days
    for i in range(6, -1, -1):
        check_date = today - timedelta(days=i)
        labels.append(check_date.strftime('%a'))  # Mon, Tue, etc.
        
        # Date range for this day
        start_of_day = datetime.combine(check_date, datetime.min.time())
        end_of_day = datetime.combine(check_date, datetime.max.time())
        start_of_day = timezone.make_aware(start_of_day)
        end_of_day = timezone.make_aware(end_of_day)
        
        # Food logs
        logs = UserFoodLog.objects.filter(
            user=request.user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        )
        daily_calories = sum(log.food_item.calories * log.quantity for log in logs)
        daily_protein = sum(log.food_item.protein * log.quantity for log in logs)
        
        # Water logs
        water_logs = WaterLog.objects.filter(
            user=request.user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        )
        daily_water = sum(log.amount_ml for log in water_logs) / 1000  # Convert to liters
        
        calories_data.append(daily_calories)
        protein_data.append(daily_protein)
        water_data.append(daily_water)
    
    context = {
        'labels': labels,
        'calories_data': calories_data,
        'protein_data': protein_data,
        'water_data': water_data,
    }
    
    return render(request, 'analytics.html', context)

@login_required
def add_water(request):
    if request.method == 'POST':
        amount_ml = int(request.POST.get('amount', 250))
        WaterLog.objects.create(user=request.user, amount_ml=amount_ml)
        return redirect('diary')
    return redirect('diary')

# Calorie burn rates per minute (approximate for average adult)
EXERCISE_CALORIES = {
    'Running': 10,
    'Cycling': 7,
    'Walking': 4,
    'Swimming': 8,
    'Weight Training': 6,
    'Yoga': 3,
    'HIIT': 12,
    'Dancing': 5,
    'Sports': 7,
    'Other': 5,
}

@login_required
def add_exercise(request):
    if request.method == 'POST':
        exercise_type = request.POST.get('exercise_type')
        duration = int(request.POST.get('duration', 30))
        notes = request.POST.get('notes', '')
        
        # Calculate calories burned
        calories_per_min = EXERCISE_CALORIES.get(exercise_type, 5)
        calories_burned = calories_per_min * duration
        
        ExerciseLog.objects.create(
            user=request.user,
            exercise_type=exercise_type,
            duration_minutes=duration,
            calories_burned=calories_burned,
            notes=notes
        )
        return redirect('diary')
    return redirect('diary')

@login_required
def export_csv(request):
    """Export last 7 days of nutrition data as CSV"""
    from datetime import datetime, timedelta
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calnut_nutrition_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Meal Type', 'Food', 'Quantity', 'Calories', 'Protein', 'Carbs', 'Fat'])
    
    # Get last 7 days of logs
    seven_days_ago = timezone.now() - timedelta(days=7)
    logs = UserFoodLog.objects.filter(
        user=request.user,
        date_added__gte=seven_days_ago
    ).order_by('-date_added')
    
    for log in logs:
        writer.writerow([
            log.date_added.strftime('%Y-%m-%d %H:%M'),
            log.meal_type,
            log.food_item.name,
            log.quantity,
            log.food_item.calories * log.quantity,
            log.food_item.protein * log.quantity,
            log.food_item.carbs * log.quantity,
            log.food_item.fat * log.quantity,
        ])
    
    return response

@login_required
def export_pdf(request):
    """Export last 7 days of nutrition summary as PDF"""
    from datetime import datetime, timedelta
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="calnut_nutrition_report.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#16a34a'),  # Green
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6b7280'),  # Gray
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Title with emoji effect
    title = Paragraph("🥗 Calnut Nutrition Report", title_style)
    elements.append(title)
    
    # User info
    username = Paragraph(f"<b>User:</b> {request.user.username}", subtitle_style)
    elements.append(username)
    
    # Date range with styling
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    date_range = Paragraph(
        f"<b>Period:</b> {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", 
        subtitle_style
    )
    elements.append(date_range)
    elements.append(Spacer(1, 20))
    
    # Section header
    section_header = Paragraph("📊 7-Day Nutrition Summary", section_style)
    elements.append(section_header)
    elements.append(Spacer(1, 12))
    
    # Daily summary table with enhanced styling
    data = [['📅 Date', '🔥 Calories', '💪 Protein', '💧 Water', '🏃 Exercise']]
    
    for i in range(6, -1, -1):
        check_date = (end_date - timedelta(days=i)).date()
        start_of_day = datetime.combine(check_date, datetime.min.time())
        end_of_day = datetime.combine(check_date, datetime.max.time())
        start_of_day = timezone.make_aware(start_of_day)
        end_of_day = timezone.make_aware(end_of_day)
        
        # Food logs
        logs = UserFoodLog.objects.filter(
            user=request.user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        )
        daily_calories = sum(log.food_item.calories * log.quantity for log in logs)
        daily_protein = sum(log.food_item.protein * log.quantity for log in logs)
        
        # Water logs
        water_logs = WaterLog.objects.filter(
            user=request.user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        )
        daily_water = sum(log.amount_ml for log in water_logs) / 1000
        
        # Exercise logs
        exercise_logs = ExerciseLog.objects.filter(
            user=request.user,
            date_added__gte=start_of_day,
            date_added__lte=end_of_day
        )
        daily_exercise = sum(log.calories_burned for log in exercise_logs)
        
        data.append([
            check_date.strftime('%a, %m/%d'),
            f'{daily_calories:.0f} kcal',
            f'{daily_protein:.1f}g',
            f'{daily_water:.1f}L',
            f'{daily_exercise:.0f} kcal'
        ])
    
    table = Table(data, colWidths=[1.4*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    
    # Enhanced table styling with gradients and modern design
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a34a')),  # Green header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows - alternating colors
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f0fdf4')),  # Light green
        ('BACKGROUND', (0, 2), (-1, 2), colors.white),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f0fdf4')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.white),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#f0fdf4')),
        ('BACKGROUND', (0, 6), (-1, 6), colors.white),
        ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor('#f0fdf4')),
        
        # Font styling for data
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#15803d')),  # Thick line under header
        
        # Rounded corners effect
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Footer note
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#9ca3af'),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    footer = Paragraph(
        "Generated by Calnut - Your Personal Nutrition Tracker 🌟<br/>Keep tracking, keep improving!",
        footer_style
    )
    elements.append(footer)
    
    doc.build(elements)
    
    return response
