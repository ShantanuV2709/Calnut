from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    fiber = models.FloatField(default=0)  # [NEW]
    sugar = models.FloatField(default=0)  # [NEW]
    category = models.CharField(max_length=100, default='General')
    image = models.URLField(blank=True, null=True)
    api_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.IntegerField()
    type = models.CharField(max_length=50) # e.g., 'high_protein', 'vegetarian'
    prep_time = models.IntegerField(default=15) # [NEW] Minutes
    difficulty = models.CharField(max_length=20, default='Easy') # [NEW] Easy, Medium, Hard
    image = models.URLField()

    def __str__(self):
        return self.name

class UserFoodLog(models.Model):
    # This acts as a junction table but for NoSQL we can also embed, 
    # but sticking to relational style for Django Admin compatibility is easier with Djongo.
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1) # e.g., number of servings or grams? Let's assume servings for now
    
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='Snack')
    
    date_added = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='meal_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name}"

class WaterLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount_ml = models.IntegerField(default=250)  # milliliters
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_ml}ml"

class ExerciseLog(models.Model):
    EXERCISE_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Walking', 'Walking'),
        ('Swimming', 'Swimming'),
        ('Weight Training', 'Weight Training'),
        ('Yoga', 'Yoga'),
        ('HIIT', 'HIIT'),
        ('Dancing', 'Dancing'),
        ('Sports', 'Sports'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_CHOICES)
    duration_minutes = models.IntegerField()  # Duration in minutes
    calories_burned = models.FloatField()  # Calculated based on activity
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} ({self.duration_minutes}min)"

