from django.shortcuts import render, redirect
import os
import requests
from .models import *
from django.contrib import messages
import pymysql
from better_profanity import profanity
import bcrypt
import json
from json import JSONEncoder
import smtplib
# Create your views here.


# render home page
def index(request):
  return render(request, 'index.html')

# post route to login
def login(request):
  # check for errors
  errors = validate_login(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/')
  else:
    # connect to db and find user with username 
    mysql = MySQLConnection('trvl-trak')
    query = 'SELECT * FROM user WHERE username = %(username)s'
    data = {
      'username': request.POST['username']
    }
    user = mysql.query_db(query, data)
    # if valid user, check to see if password matches
    if user:
      user = user[0]
      # if password matches, add user to session and redirect to dash
      if bcrypt.checkpw(request.POST['password'].encode(), user['password'].encode()):
        request.session['user_id'] = user['id']
        return redirect('/dashboard')
      else:
        messages.error(request, "Password does not match")
    return redirect('/')

# logout 
def logout(request):
  # clear session
  request.session.flush()
  return redirect('/')

# post route to handle registration
def register(request):
  # check for errors
  errors = validate_registration(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/')
  # if valid info, hash & salt the password and add user to db
  elif request.POST['password'] == request.POST['conf_password']:
    password = request.POST['password']
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # create user
    mysql = connectToMySQL('trvl-trak')
    # add user to db
    query = 'INSERT INTO user (first_name, last_name, username, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(password)s, NOW(), NOW())'
    data = {
      'first_name': request.POST['first_name'],
      'last_name': request.POST['last_name'],
      'username': request.POST['username'],
      'password': password_hash,
    }
    user_id = mysql.query_db(query, data)
    request.session['user_id'] = user_id
    request.session['location'] = 'Chicago, IL'
    return redirect('/dashboard')

# email contact 
def contact(request):
  errors = validate_contact(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.warning(request, val)
    return redirect('/#contact')
  else: 
    # send message to email
    with smtplib.SMTP('smtp.gmail.com', 587) as smpt:
      
      email_address = 'trvltrak@gmail.com'
      name = request.POST['name']
      user_email = request.POST['contact-email']
      user_message = request.POST['message']

      smpt.ehlo()
      smpt.starttls()
      smpt.ehlo()
      
      smpt.login(email_address, os.environ.get('TRVL_EMAIL_PASS'))
      
      subject = f'New Message from {name}, {user_email}'
      body = user_message

      message = f'Subject: {subject}\n\n{body}'

      smpt.sendmail(email_address, email_address, message)
    
      messages.success(request, 'Email Successfully sent!')
    return redirect('/')

# encode datetime objects
def endodeDate(d):
  if isinstance(d, (datetime.date, datetime.datetime)):
    return d.isoformat()

# dashboard
def dashboard(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    # return saved trips
    mysql = MySQLConnection('trvl-trak')
    query = 'SELECT * FROM trip WHERE user_id = %(user_id)s'
    data = {
      'user_id': request.session['user_id']
    }
    trips = mysql.query_db(query, data)
    print(trips)
    for t in trips:
      t['trip_start'] = t['trip_start'].strftime('%m/%d/%Y')
      t['trip_end'] = t['trip_end'].strftime('%m/%d/%Y')
      t['created_at'] = t['created_at'].strftime('%m/%d/%Y')
      t['updated_at'] = t['updated_at'].strftime('%m/%d/%Y')

    # return google map
    context = {
      'key': os.environ.get('GOOGLE_API_KEY'),
      'json_trips': json.dumps(trips),
      'trips': trips
    }
    return render(request, 'dashboard.html', context)
    
# search
def search(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    # return google map
    context = {
      'key': os.environ.get('GOOGLE_API_KEY')
    }
    return render(request, 'search.html', context)

# post request to handle api geocoding
def getLatLng(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    # get lat and lng from google maps api
    if request.POST['location-input'] == '':
      request.session['location'] = 'Chicago, IL'
      return redirect('/search')
    else:
      request.session['location'] = request.POST['location-input']
      return redirect('/search')

# add to favorites
def addFav(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    # validate address, lat, lng
    address = request.GET.get('address')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if lat == None or lng == None or address == None:
      return redirect('/dashboard')
    try:
      lat = float(lat)
      lng = float(lng)
    except ValueError:
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
    # check for errors
    errors = validate_form(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect('/search')
    elif request.POST['trip-start'] <= request.POST['trip-end']:
      mysql = MySQLConnection('trvl-trak')
      query = 'INSERT INTO trip (title, address, latitude, longitude, trip_start, trip_end, description, created_at, updated_at, user_id) VALUES (%(title)s, %(address)s, %(latitude)s, %(longitude)s, %(trip_start)s, %(trip_end)s, %(description)s, NOW(), NOW(), %(user_id)s)'
      data = {
        'title': request.POST['title'],
        'address': request.POST['address'],
        'latitude': request.POST['lat'],
        'longitude': request.POST['lng'],
        'trip_start': request.POST['trip-start'],
        'trip_end': request.POST['trip-end'],
        'description': request.POST['description'],
        'user_id': request.session['user_id'],
      }
      new_trip_id = mysql.query_db(query, data)
      # message.success(request, 'Successfully Added New Trip!')
      return redirect('/dashboard')
    else:
      return redirect('/search')

