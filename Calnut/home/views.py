
from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    context={
        'variable':'This is sent'
    }
    return render(request,'home.html',context)
    #return HttpResponse ('This is Home page.')

def about(request):
    return render(request,'about.html')
    #return HttpResponse ('This is About page.')

def nutrition(request):
    return render(request,'nutrition.html')
    #return HttpResponse('This is nutrition page.')    

def calories(request):
    return render(request, 'calories.html')

def graphs(request):
    return render(request, 'graphs.html')

def meals(request):
    meals = [
        {
            'name': 'Grilled Chicken Salad',
            'description': 'Lean grilled chicken breast served with fresh greens, cherry tomatoes, and a light vinaigrette.',
            'calories': 400,
            'protein': 35,
            'type': 'high_protein',
            'image': 'https://www.licious.in/blog/wp-content/uploads/2020/12/Grilled-Chicken-Salad-min.jpg'
        },
        {
            'name': 'Oats and Berries Bowl',
            'description': 'Rolled oats cooked in almond milk, topped with blueberries, banana slices, and chia seeds.',
            'calories': 350,
            'protein': 10,
            'type': 'vegetarian',
            'image': 'https://images.squarespace-cdn.com/content/v1/54358a91e4b0d0810faf81fe/1456770904251-X8RMF2K5MDFUAW7J18TJ/spring-berry-oatmeal-bowl.jpg'
        },
        {
            'name': 'Veggie Stir-fry with Tofu',
            'description': 'Colorful bell peppers, broccoli, and tofu sautéed in sesame oil and garlic.Serve over rice or on its own.',
            'calories': 450,
            'protein': 22,
            'type': 'low_carb',
            'image': 'https://www.bitesofberi.com/wp-content/uploads/2020/12/veggie-tofu-stir-fry-1.jpg'
        },
    ]
    return render(request, 'meals.html', {'meals': meals})


def food(request):
    food_items = [
        {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "category": "Fruits"},
        {"name": "Grilled Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "category": "Protein"},
        {"name": "Brown Rice", "calories": 215, "protein": 5, "carbs": 45, "fat": 1.8, "category": "Grains"},
        {"name": "Broccoli", "calories": 55, "protein": 3.7, "carbs": 11.2, "fat": 0.6, "category": "Vegetables"},
        {"name": "Almonds", "calories": 164, "protein": 6, "carbs": 6, "fat": 14, "category": "Nuts"},
        {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.3, "category": "Fruits"},
        {"name": "Egg", "calories": 78, "protein": 6, "carbs": 0.6, "fat": 5, "category": "Protein"},
        {"name": "Paneer Butter Masala", "calories": 350, "protein": 18, "carbs": 20, "fat": 25, "category": "Main Course"},
        {"name": "Idli", "calories": 58, "protein": 2, "carbs": 12, "fat": 0.4, "category": "Breakfast"},
        {"name": "Samosa", "calories": 132, "protein": 3, "carbs": 17, "fat": 6, "category": "Snacks"},
        {"name": "Masala Dosa", "calories": 168, "protein": 4, "carbs": 25, "fat": 6, "category": "Breakfast"},
        {"name": "Chicken Biryani", "calories": 360, "protein": 20, "carbs": 40, "fat": 15, "category": "Main Course"},
        {"name": "Gulab Jamun", "calories": 150, "protein": 2, "carbs": 25, "fat": 7, "category": "Dessert"},
    ]
    return render(request, 'food.html', {'food_items': food_items})

def recipes(request):
    return render(request, 'recipes.html')

def blogs(request):
    return render(request, 'blogs.html')