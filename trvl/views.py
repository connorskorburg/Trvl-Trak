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
  print(request.POST['location-input'])
  url = ''
  return redirect('/dashboard')