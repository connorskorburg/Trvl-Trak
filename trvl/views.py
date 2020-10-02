from django.shortcuts import render, redirect
import os
import requests
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