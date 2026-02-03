import requests
from .models import FoodItem, Meal

def fetch_food_data(query):
    """
    Fetches food data from OpenFoodFacts API.
    """
    # Sort by popularity (unique_scans_n) to get most common items first
    # Limit to 10 results to prevent flooding the DB with junk
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1&sort_by=unique_scans_n&page_size=10"
    headers = {
        'User-Agent': 'Calnut/1.0 (calnut_app@example.com)'  # Required by OpenFoodFacts
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            results = []
            for product in products:
                # Extract relevant fields with safe defaults
                nutriments = product.get('nutriments', {})
                
                item = {
                    'name': product.get('product_name', 'Unknown'),
                    'calories': nutriments.get('energy-kcal_100g', 0),
                    'protein': nutriments.get('proteins_100g', 0),
                    'carbs': nutriments.get('carbohydrates_100g', 0),
                    'fat': nutriments.get('fat_100g', 0),
                    'fiber': nutriments.get('fiber_100g', 0),    # [NEW]
                    'sugar': nutriments.get('sugars_100g', 0),   # [NEW]
                    'category': product.get('categories_tags', ['Unknown'])[0] if product.get('categories_tags') else 'Unknown',
                    'image': product.get('image_front_small_url', ''),
                    'api_id': product.get('code', '')
                }
                results.append(item)
            return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    return []

def seed_database():
    """
    Seeds the database with common food items and meals if they don't exist.
    """
    
    # --- 1. Seed Food Items ---
    if FoodItem.objects.count() > 0:
        print("Food Items already seeded. Checking for updates...")
        
    print("Seeding/Updating Food Items...")
    manual_foods = [
        {"name": "Apple", "calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4, "sugar": 10, "category": "Fruits", "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500&auto=format&fit=crop&q=60"},
        {"name": "Banana", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6, "sugar": 12, "category": "Fruits", "image": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=500&auto=format&fit=crop&q=60"},
        {"name": "Watermelon", "calories": 30, "protein": 0.6, "carbs": 8, "fat": 0.2, "fiber": 0.4, "sugar": 6, "category": "Fruits", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&auto=format&fit=crop&q=60"},
        {"name": "Kiwi", "calories": 61, "protein": 1.1, "carbs": 15, "fat": 0.5, "fiber": 3, "sugar": 9, "category": "Fruits", "image": "https://images.unsplash.com/photo-1585059895524-72359e06138a?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pizza", "calories": 266, "protein": 11, "carbs": 33, "fat": 10, "fiber": 2.3, "sugar": 3.6, "category": "Fast Food", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=60"},
        {"name": "Burger", "calories": 295, "protein": 17, "carbs": 30, "fat": 14, "fiber": 1.6, "sugar": 4.2, "category": "Fast Food", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pasta", "calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "fiber": 1.2, "sugar": 0.6, "category": "Grains", "image": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500&auto=format&fit=crop&q=60"},
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sugar": 0, "category": "Protein", "image": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500&auto=format&fit=crop&q=60"},
        {"name": "Brown Rice", "calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9, "fiber": 1.8, "sugar": 0.4, "category": "Grains", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=60"},
        {"name": "Avocado", "calories": 160, "protein": 2, "carbs": 8.5, "fat": 15, "fiber": 6.7, "sugar": 0.7, "category": "Vegetables", "image": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=500&auto=format&fit=crop&q=60"},
        {"name": "Egg", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0, "sugar": 1.1, "category": "Protein", "image": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=500&auto=format&fit=crop&q=60"},
        {"name": "Almonds", "calories": 579, "protein": 21, "carbs": 22, "fat": 50, "fiber": 12.5, "sugar": 4.4, "category": "Nuts", "image": "https://images.unsplash.com/photo-1613728917105-26dbc1126d42?w=500&auto=format&fit=crop&q=60"},
        {"name": "Broccoli", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6, "sugar": 1.7, "category": "Vegetables", "image": "https://images.unsplash.com/photo-1459411621453-7fb7e6e5b6fa?w=500&auto=format&fit=crop&q=60"},
    ]

    for data in manual_foods:
        if not FoodItem.objects.filter(name=data['name']).exists():
            FoodItem.objects.create(
                name=data['name'],
                calories=data['calories'],
                protein=data['protein'],
                carbs=data['carbs'],
                fat=data['fat'],
                fiber=data.get('fiber', 0),
                sugar=data.get('sugar', 0),
                category=data['category'],
                image=data['image'],
                api_id='manual'
            )
            print(f"Added {data['name']}")
        
        # Try dynamic fetching for extra items
        extra_foods = ['Milk', 'Salmon']
        for food in extra_foods:
            print(f"Attempting to fetch {food} from API...")
            results = fetch_food_data(food)
            if results:
                data = results[0]
                FoodItem.objects.create(
                    name=data['name'],
                    calories=data['calories'],
                    protein=data['protein'],
                    carbs=data['carbs'],
                    fat=data['fat'],
                    category=data['category'],
                    image=data['image'],
                    api_id=data['api_id']
                )
                print(f"Added {data['name']} (API)")
            else:
                print(f"Skipped {food} (API failed)")

    # --- 2. Seed Meals ---
    if Meal.objects.count() > 0:
        print("Meals already seeded.")
    else:
        print("Seeding Meals...")
        meals = [
            {
                "name": "Grilled Chicken Salad",
                "type": "Lunch",
                "calories": 450,
                "protein": 40,
                "description": "A high-protein salad with grilled chicken breast, mixed greens, cherry tomatoes, and balsamic vinaigrette.",
                "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=60"
            },
            {
                "name": "Oatmeal with Berries",
                "type": "Breakfast",
                "calories": 350,
                "protein": 12,
                "description": "Warm oats topped with fresh strawberries, blueberries, and a drizzle of honey.",
                "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=500&auto=format&fit=crop&q=60"
            },
            {
                "name": "Salmon with Asparagus",
                "type": "Dinner",
                "calories": 550,
                "protein": 45,
                "description": "Pan-seared salmon fillet served with roasted asparagus and lemon butter sauce.",
                "image": "https://images.unsplash.com/photo-1467003909585-2f8a7270028d?w=500&auto=format&fit=crop&q=60"
            },
            {
                "name": "Greek Yogurt Parfait",
                "type": "Snack",
                "calories": 200,
                "protein": 15,
                "description": "Layers of greek yogurt, granola, and honey. Perfect for a quick energy boost.",
                "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&auto=format&fit=crop&q=60"
            }
        ]
        
        for meal in meals:
            Meal.objects.create(
                name=meal['name'],
                type=meal['type'],
                calories=meal['calories'],
                protein=meal['protein'],
                description=meal['description'],
                image=meal['image']
            )
            print(f"Added Meal: {meal['name']}")
