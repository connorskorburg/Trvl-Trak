from django.shortcuts import render, redirect
import os
import requests
from .models import *
from django.contrib import messages
import pymysql
from better_profanity import profanity
import bcrypt
# Create your views here.


# render home page
def index(request):
  return render(request, 'index.html')

# post route to login
def login(request):
  errors = validate_login(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      print(key, val)
      messages.error(request, val)
    return redirect('/')
  else:
    mysql = MySQLConnection('trvl-trak')
    query = 'SELECT * FROM user WHERE username = %(username)s'
    data = {
      'username': request.POST['username']
    }
    user = mysql.query_db(query, data)
    if user:
      user = user[0]
      if bcrypt.checkpw(request.POST['password'].encode(), user['password'].encode()):
        request.session['user_id'] = user['id']
        return redirect('/dashboard')
      else:
        messages.error(request, "Password does not match")
    return redirect('/')

# logout 
def logout(request):
  request.session.flush()
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
  elif request.POST['password'] == request.POST['conf_password']:
    password = request.POST['password']
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # create user
    mysql = connectToMySQL('trvl-trak')
    query = 'INSERT INTO user (first_name, last_name, username, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(password)s, NOW(), NOW())'
    data = {
      'first_name': request.POST['first_name'],
      'last_name': request.POST['last_name'],
      'username': request.POST['username'],
      'password': password_hash,
    }
    user_id = mysql.query_db(query, data)
    request.session['user_id'] = user_id
    print('successful info')
    return redirect('/dashboard')


# dashboard
def dashboard(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    context = {
      'key': os.environ.get('GOOGLE_API_KEY')
    }
    return render(request, 'dashboard.html', context)
    
# search
def search(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    context = {
      'key': os.environ.get('GOOGLE_API_KEY')
    }
    return render(request, 'search.html', context)

# post request to handle api geocoding
def getLatLng(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    request.session['location'] = request.POST['location-input']
    return redirect('/search')

# add to favorites
def addFav(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
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
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    print(request.POST)
    errors = validate_form(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect('/search')
    else:
      return redirect('/dashboard')


