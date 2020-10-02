from django.shortcuts import render, redirect
import os
import requests
from .models import *
from django.contrib import messages
import pymysql
# Create your views here.


# render home page
def index(request):
  return render(request, 'index.html')

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