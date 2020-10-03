from django.shortcuts import render, redirect
import os
import requests
from .models import *
from django.contrib import messages
import pymysql
from better_profanity import profanity
# Create your views here.


# render home page
def index(request):
  return render(request, 'index.html')

# post route to login
def login(request):
  print(request.POST)
  errors = validate_login(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      print(key, val)
      messages.error(request, val)
    return redirect('/')
  return redirect('/')

# post route to handle registration
def register(request):
  print(request.POST)
  errors = validate_registration(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      print(key, val)
      messages.error(request, val)
    return redirect('/')
  return redirect('/')


# dashboard
def dashboard(request):
  context = {
    'key': os.environ.get('GOOGLE_API_KEY')
  }
  return render(request, 'dashboard.html', context)
# dashboard
def search(request):
  context = {
    'key': os.environ.get('GOOGLE_API_KEY')
  }
  return render(request, 'search.html', context)

# post request to handle api geocoding
def getLatLng(request):
  request.session['location'] = request.POST['location-input']
  return redirect('/search')

# add to favorites
def addFav(request):
  print(request)

  address = request.GET.get('address')
  lat = request.GET.get('lat')
  lng = request.GET.get('lng')

  if lat == None or lng == None or address == None:
    return redirect('/')
  try:
    lat = float(lat)
    lng = float(lng)
    print(True)
  except ValueError:
    print(False)
    return redirect('/search')

  if lat > 90 or lat < -90 or lng > 180 or lng < -180 or address == '':
    return redirect('/search')
  else:
    context = {
      'address': address,
      'lat': lat,
      'lng': lng
    }
    return render(request, 'newFav.html', context)


# add new favorite
def newFav(request):
  print(request.POST)
  errors = validate_form(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/search')
  else:
    return redirect('/dashboard')


# VALIDATIONS


#validate new favorite trip data
def validate_form(post_data):
  errors = {}
  
  if post_data['address'] == '':
    errors['address'] = "Please Enter Valid Address"
  
  if post_data['lng'] == '' or  float(post_data['lng']) > 180 or float(post_data['lng']) < -180:
    errors['lng'] = 'Please Enter Valid Longitude'

  if post_data['lat'] == '' or float(post_data['lat']) > 90 or float(post_data['lat']) < -90:
    errors['lat'] = 'Please Enter Valid Latitude'

  if post_data['trip-start'] == '':
    errors['trip-start'] = 'Please Enter Valid Start Date'  

  if post_data['trip-end'] == '':
    errors['trip-end'] = 'Please Enter Valid End Date'

  if post_data['description'] == '':
    errors['description'] = 'Please Enter Valid Description'

  return errors

# validate registration 
def validate_registration(post_data):
  errors = {}

  if len(post_data['first_name']) > 1 or post_data['first_name'] == '':
    errors['first_name'] = "First Name must contain 2 letters or more" 

  if profanity.contains_profanity(post_data['first_name']) == True:
    errors['bad_first_name'] = "Please Enter an appropriate First Name"

  if len(post_data['last_name']) > 1 or post_data['last_name'] == '':
    errors['last_name'] = "Last Name must contain 2 letters or more"

  if profanity.contains_profanity(post_data['last_name']) == True:
    errors['last_name'] = "Please Enter an appropriate Last Name"

  if len(post_data['username']) > 4 or post_data['username'] == '':
    errors['username'] = "Username must contain 5 letters or more"

  if profanity.contains_profanity(post_data['username']) == True:
    errors['bad_username'] = "Please Enter an appropriate username"

  if len(post_data['password']) > 7 or post_data['password'] == '':
    errors['password'] = "Password must contain 8 characters or more"

  if post_data['password'] != post_data['conf_password']:
    errors['conf_password'] = "Passwords do not match"

  return errors
  
# validate login 
def validate_login(post_data):
  errors = {}

  if len(post_data['username']) > 4 or post_data['username'] == '':
    errors['username'] = "Please Enter valid username"

  if len(post_data['password']) > 7 or post_data['password'] == '':
    errors['password'] = "Please Enter valid password"

  return errors
