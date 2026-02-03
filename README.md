# 🥗 Calnut - Personal Nutrition Tracker

A comprehensive Django-based nutrition tracking web application that helps users monitor their daily calorie intake, protein consumption, water intake, and exercise activities. Built with Django and MongoDB, Calnut provides an intuitive interface for managing your health and fitness goals.

![Django](https://img.shields.io/badge/Django-3.1.12-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📊 Core Functionality
- **Food Database**: Extensive food database with nutritional information (calories, protein, carbs, fats, fiber, sugar)
- **Food Logging**: Track your meals by type (Breakfast, Lunch, Dinner, Snack) with customizable quantities
- **Photo Logging**: Attach photos to your meal entries for visual tracking
- **API Integration**: Automatic food data fetching from external APIs when searching for new items
- **Meal Planner**: Browse and discover pre-made meal suggestions with nutritional information

### 💧 Health Tracking
- **Water Intake**: Log and track daily water consumption with progress indicators
- **Exercise Logging**: Record various exercise types with automatic calorie burn calculations
- **Streak Tracking**: Maintain your logging streak to build consistent habits
- **Net Calories**: Automatic calculation of net calories (consumed - burned)

### 📈 Analytics & Insights
- **7-Day Analytics**: Visual charts showing calorie, protein, and water intake trends
- **Daily Progress**: Real-time progress bars for calories, protein, and water goals
- **BMR/TDEE Calculator**: Automatic calculation of Basal Metabolic Rate and Total Daily Energy Expenditure
- **Goal Setting**: Personalized calorie and protein goals based on user profile

### 👤 User Profile Management
- **Detailed Profiles**: Track weight, height, gender, age, and activity level
- **Profile Pictures**: Upload custom profile pictures
- **Goal Tracking**: Set and monitor current weight vs. goal weight
- **Activity Levels**: Choose from sedentary to extra active lifestyle settings

### 📤 Export & Reports
- **CSV Export**: Download your nutrition data for the last 7 days in CSV format
- **PDF Reports**: Generate beautifully styled PDF reports with weekly nutrition summaries
- **Visual Reports**: Professional PDF layouts with emoji icons and color-coded tables

## 🛠️ Technology Stack

- **Backend**: Django 3.1.12
- **Database**: MongoDB (via Djongo)
- **ORM**: Djongo 1.3.7 (Django-MongoDB connector)
- **PDF Generation**: ReportLab
- **Authentication**: Django built-in authentication system
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x
- MongoDB (version 3.x or higher)
- pip (Python package installer)

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Calnut
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Additional Dependencies
The `requirements.txt` includes core dependencies. You may also need:
```bash
pip install Pillow  # For image handling
pip install reportlab  # For PDF generation
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root directory:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Then edit the `.env` file and update the following values:
```env
DJANGO_SECRET_KEY=your-generated-secret-key-here
DEBUG=True
```

> [!TIP]
> Generate a secure secret key using Python:
> ```python
> from django.core.management.utils import get_random_secret_key
> print(get_random_secret_key())
> ```

### 6. Configure MongoDB

Ensure MongoDB is running on your local machine:
```bash
# Windows
net start MongoDB

# macOS/Linux
sudo systemctl start mongod
```

The default MongoDB connection is configured in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'Calnut',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}
```

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create a Superuser
```bash
python manage.py createsuperuser
```

### 9. Create Required Directories
```bash
# Windows
mkdir media\meal_photos
mkdir media\profile_pics
mkdir static
mkdir staticfiles

# macOS/Linux
mkdir -p media/meal_photos
mkdir -p media/profile_pics
mkdir static
mkdir staticfiles
```

### 10. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
Calnut/
├── Calnut/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── accounts/            # User authentication and profiles
│   ├── models.py        # UserProfile model
│   ├── views.py         # Authentication views
│   ├── forms.py         # User forms
│   └── admin.py         # Admin configuration
├── home/                # Main application logic
│   ├── models.py        # FoodItem, Meal, UserFoodLog, WaterLog, ExerciseLog
│   ├── views.py         # Core views and business logic
│   ├── utils.py         # Helper functions (API integration)
│   └── admin.py         # Admin configuration
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── home.html        # Landing page
│   ├── food.html        # Food search
│   ├── diary.html       # Daily food diary
│   ├── meals.html       # Meal suggestions
│   ├── calories.html    # Calorie calculator
│   └── analytics.html   # Analytics dashboard
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploads
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🎯 Usage

### Creating a User Profile
1. Register a new account or login
2. Navigate to your profile
3. Fill in your details:
   - Current weight and goal weight
   - Height
   - Gender
   - Activity level
   - Date of birth

### Logging Food
1. Go to **Food** section
2. Search for a food item (searches local DB and external API)
3. Click "Add to Diary"
4. Select meal type (Breakfast, Lunch, Dinner, Snack)
5. Adjust quantity as needed
6. Optionally upload a photo

### Tracking Water
1. Navigate to **Diary**
2. Use the "Log Water" button
3. Select amount (default 250ml)

### Logging Exercise
1. Go to **Diary**
2. Click "Add Exercise"
3. Select exercise type
4. Enter duration in minutes
5. Calories burned are automatically calculated

### Viewing Analytics
1. Navigate to **Analytics**
2. View 7-day trends for:
   - Calories consumed
   - Protein intake
   - Water consumption

### Exporting Data
1. Go to **Diary** or **Analytics**
2. Choose export format:
   - **CSV**: Raw data export
   - **PDF**: Formatted report with styling

## 🧪 Exercise Calorie Calculations

The application uses approximate calorie burn rates per minute:

| Exercise Type     | Calories/Minute |
|------------------|-----------------|
| Running          | 10              |
| HIIT             | 12              |
| Swimming         | 8               |
| Cycling          | 7               |
| Sports           | 7               |
| Weight Training  | 6               |
| Dancing          | 5               |
| Other            | 5               |
| Walking          | 4               |
| Yoga             | 3               |

## 📊 Database Models

### FoodItem
- `name`: Food item name
- `calories`, `protein`, `carbs`, `fat`, `fiber`, `sugar`: Nutritional values
- `category`: Food category
- `image`: Food image URL
- `api_id`: External API identifier

### UserFoodLog
- Links users to food items
- Tracks quantity, meal type, and timestamp
- Supports photo uploads

### WaterLog
- Tracks water intake in milliliters
- Timestamped entries

### ExerciseLog
- Exercise type and duration
- Automatic calorie burn calculation
- Optional notes field

### UserProfile
- Personal information (weight, height, age, gender)
- Activity level and goals
- BMR/TDEE calculations
- Profile picture

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues

- Djongo has limited support for complex Django ORM queries
- Some date-based queries use workarounds due to Djongo limitations
- Random sorting (`order_by('?')`) is not supported with Djongo

## 🔮 Future Enhancements

- [ ] Mobile app (React Native or Flutter)
- [ ] Barcode scanning for food items
- [ ] Social features (share progress, challenges)
- [ ] Recipe builder with nutritional calculation
- [ ] Integration with fitness trackers (Fitbit, Apple Health)
- [ ] Advanced meal planning with weekly schedules
- [ ] Macro tracking (beyond calories and protein)
- [ ] Custom food creation
- [ ] Weight progress tracking with charts
- [ ] Notification system for reminders

## 📧 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## 🙏 Acknowledgments

- Django community for excellent documentation
- Djongo for MongoDB-Django integration
- ReportLab for PDF generation capabilities
- External nutrition APIs for food data

---

**Made with ❤️ and Django**

*Stay healthy, stay happy! 🌟*
