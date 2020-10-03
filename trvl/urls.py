from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('search', views.search),
    path('getLatLng', views.getLatLng),
    path('addFav', views.addFav),
    path('newFav', views.newFav),
    path('login', views.login),
    path('register', views.register),
]