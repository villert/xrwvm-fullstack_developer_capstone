# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt
import os

# helper to load JSON data from server/database/data
def _load_data(filename):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'data'))
    path = os.path.join(base, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)
ADDED_REVIEWS = []


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


@csrf_exempt
def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    password = data.get('password', '')

    if not all([username, first_name, last_name, email, password]):
        return JsonResponse({"status": "Invalid request", "message": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "User exists", "message": "Username already exists"}, status=409)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "User created"})


def get_dealerships(request):
    data = _load_data('dealerships.json')
    dealerships = data.get('dealerships', [])
    return JsonResponse({'status': 200, 'dealers': dealerships, 'dealerships': dealerships})


def get_dealer_details(request, dealer_id):
    data = _load_data('dealerships.json')
    dealers = data.get('dealerships', [])
    for d in dealers:
        if int(d.get('id')) == int(dealer_id):
            response = dict(d)
            response.update({'status': 200, 'dealer': [d]})
            return JsonResponse(response)
    return JsonResponse({'status': 404, 'dealer': []}, status=404)


def get_dealers_by_state(request, state):
    data = _load_data('dealerships.json')
    dealers = data.get('dealerships', [])
    if state.lower() == 'all':
        return JsonResponse({'status': 200, 'dealers': dealers, 'dealerships': dealers})
    state_lower = state.lower()
    matched = [d for d in dealers if d.get('state','').lower() == state_lower or d.get('st','').lower() == state_lower]
    return JsonResponse({'status': 200, 'dealers': matched, 'dealerships': matched})


def get_dealer_reviews(request, dealer_id):
    data = _load_data('reviews.json')
    reviews = data.get('reviews', []) + ADDED_REVIEWS
    matched = [r for r in reviews if int(r.get('dealership')) == int(dealer_id)]
    return JsonResponse({'status': 200, 'reviews': matched})


def get_all_carmakes(request):
    data = _load_data('car_records.json')
    cars = data.get('cars', [])
    car_models = [
        {
            'CarMake': car.get('make', ''),
            'CarModel': car.get('model', ''),
            'CarYear': car.get('year', ''),
            'CarType': car.get('bodyType', ''),
        }
        for car in cars
    ]
    return JsonResponse({'status': 200, 'cars': cars, 'CarModels': car_models})


def get_cars(request):
    data = _load_data('car_records.json')
    cars = data.get('cars', [])
    car_models = [
        {
            'CarMake': car.get('make', ''),
            'CarModel': car.get('model', ''),
            'CarYear': car.get('year', ''),
            'CarType': car.get('bodyType', ''),
        }
        for car in cars
    ]
    return JsonResponse({'CarModels': car_models})


def analyze_review(request):
    # Accept GET param 'text' or JSON POST with {'text': '...'}
    text = ''
    if request.method == 'GET':
        text = request.GET.get('text','')
    else:
        try:
            data = json.loads(request.body)
            text = data.get('text','')
        except Exception:
            text = ''

    sentiment = 'neutral'
    if text and 'fantastic' in text.lower():
        sentiment = 'positive'
    elif text and any(w in text.lower() for w in ['bad','terrible','awful','poor']):
        sentiment = 'negative'

    return JsonResponse({'text': text, 'sentiment': sentiment})


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    data['id'] = len(ADDED_REVIEWS) + 10000
    data['sentiment'] = 'positive' if 'fantastic' in data.get('review', '').lower() else 'neutral'
    ADDED_REVIEWS.append(data)
    return JsonResponse({'status': 200, 'review': data})

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
