from django.shortcuts import render
#from .models import Car  
#from .forms import CarForm
from pymongo import MongoClient 
from bson.objectid import ObjectId 
from collections import Counter, defaultdict

def homepage(request):
    return render(request, 'carapp/homepage.html')

def car_list(request):
    client = MongoClient("mongodb+srv://obianefoujunwa:Ujuobi93#@bdat1004.j3asb.mongodb.net/?retryWrites=true&w=majority&appName=BDAT1004")
    db = client['bdat1004']
    collection = db['fp_group_9']

    cars = list(collection.find())

    make_list = collection.distinct('make')
    body_style_list = collection.distinct('body_style')
    engine_type_list = collection.distinct('engine_type')

    context = {
        'cars': cars,
        'make_list': make_list,
        'body_style_list': body_style_list,
        'engine_type_list': engine_type_list,
    }

    return render(request, 'carapp/car_list.html', context)

def dashboard_view(request):
    client = MongoClient("mongodb+srv://obianefoujunwa:Ujuobi93#@bdat1004.j3asb.mongodb.net/?retryWrites=true&w=majority&appName=BDAT1004")
    db = client['bdat1004']
    collection = db['fp_group_9']
    user_collection = db['user_profile']

    # Make counts
    make_counts = {}
    for car in collection.find():
        make = car.get('make', 'Unknown')
        if make in make_counts:
            make_counts[make] += 1
        else:
            make_counts[make] = 1

    cars = collection.find()

    # Visualization 3: Make to Horsepower > 200
    make_horsepower = []
    for car in cars:
        try:
            horsepower = int(car.get('horsepower', 0))  # Ensure horsepower is an integer
            if horsepower > 200:
                make_horsepower.append([car.get('make', ''), horsepower])
        except ValueError:
            continue  # Skip if conversion fails
    cars = collection.find()


    # Pie chart for Average Price by Body Type
    price_bodytype_dict = defaultdict(list)
    for car in collection.find({'price': {'$ne': None}}):
        body_type = car.get('body_style', 'Unknown')
        price = car.get('price', 0)
        try:
            price = float(price)
        except ValueError:
            price = 0.0
        price_bodytype_dict[body_type].append(price)

    # Calculate average price for each body type
    price_bodytype = [(body_type, sum(prices) / len(prices)) for body_type, prices in price_bodytype_dict.items() if len(prices) > 0]
    cars = collection.find()


    # Scatter plot for Price vs. Horsepower
    price_horsepower = []
    for car in collection.find({'price': {'$ne': None}, 'horsepower': {'$ne': None}}):
        price = car.get('price', 0)
        horsepower = car.get('horsepower', 0)
        try:
            price = float(price)
            horsepower = int(horsepower)
        except ValueError:
            price = 0.0
            horsepower = 0
        price_horsepower.append((price, horsepower))

    # User Data Processing
    users = list(user_collection.find({}))
    user_count = len(users)

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
    # Connect to the MongoDB database
    client = MongoClient("mongodb+srv://obianefoujunwa:Ujuobi93#@bdat1004.j3asb.mongodb.net/?retryWrites=true&w=majority&appName=BDAT1004")
    db = client.get_database("bdat1004")
    collection = db.user_profile

    # Retrieve all users' data
    users = list(collection.find({}, {'name': 1, 'email': 1, 'login': 1, 'phone': 1, 'picture': 1}))

    context = {
        'users': users,
    }

    return render(request, 'carapp/users_profile.html', context)

