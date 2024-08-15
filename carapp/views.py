from django.shortcuts import render
import psycopg2
from collections import Counter, defaultdict

def get_car_db_connection():
    return connections['default']  # This will use the 'default' database in settings.py

def get_user_db_connection():
    return connections['user_db']  # This will use the 'user_db' database in settings.py

def homepage(request):
    return render(request, 'carapp/homepage.html')

def car_list(request):
    conn = get_car_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars")  # Query for cars table
    cars = cursor.fetchall()
    print(cars)

    cursor.execute("SELECT DISTINCT make FROM cars")
    make_list = cursor.fetchall()

    cursor.execute("SELECT DISTINCT body_style FROM cars")
    body_style_list = cursor.fetchall()

    cursor.execute("SELECT DISTINCT engine_type FROM cars")
    engine_type_list = cursor.fetchall()

    cursor.close()
    conn.close()

    context = {
        'cars': cars,
        'make_list': make_list,
        'body_style_list': body_style_list,
        'engine_type_list': engine_type_list,
    }

    return render(request, 'carapp/car_list.html', context)

def dashboard_view(request):
    # Connect to the car database
    conn = get_car_db_connection()
    cursor = conn.cursor()

    # Make counts
    cursor.execute("SELECT make, COUNT(*) FROM cars GROUP BY make")
    make_counts = dict(cursor.fetchall())

    # Make to Horsepower > 200
    cursor.execute("""
        SELECT make, horsepower::integer 
        FROM cars 
        WHERE horsepower ~ '^[0-9]+$' AND horsepower::integer > 200
    """)
    make_horsepower = cursor.fetchall()

    # Pie chart for Average Price by Body Type
    cursor.execute("""
        SELECT body_style, AVG(price::numeric) 
        FROM cars 
        WHERE price ~ '^[0-9]+$' AND price IS NOT NULL 
        GROUP BY body_style
    """)
    price_bodytype = cursor.fetchall()

    # Scatter plot for Price vs. Horsepower
    cursor.execute("""
        SELECT price::numeric, horsepower::integer 
        FROM cars 
        WHERE price ~ '^[0-9]+$' AND horsepower ~ '^[0-9]+$' 
        AND price IS NOT NULL 
        AND horsepower IS NOT NULL
    """)
    price_horsepower = cursor.fetchall()

    cursor.close()
    conn.close()

    # Connect to the user database
    conn = get_user_db_connection()
    cursor = conn.cursor()

    # User Data Processing
    cursor.execute("SELECT * FROM user_profile")  # Ensure this table exists in the correct database
    users = cursor.fetchall()
    user_count = len(users)

    cursor.close()
    conn.close()

    context = {
        'make_counts': make_counts,
        'make_horsepower': make_horsepower,
        'price_bodytype': price_bodytype,
        'price_horsepower': price_horsepower,
        'user_count': user_count,
        'users': users,
    }

    return render(request, 'carapp/dashboard.html', context)

def users_profile(request):
    conn = get_user_db_connection()
    cursor = conn.cursor()

    # Retrieve all users' data
    cursor.execute("SELECT first_name, last_name, email, username, phone, picture FROM user_profile")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    context = {
        'users': users,
    }

    return render(request, 'carapp/users_profile.html', context)
