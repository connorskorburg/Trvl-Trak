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
    path('logout', views.logout),
    path('register', views.register),
    path('contact', views.contact),
    path('trip/delete/<int:id>', views.deleteTrip),
]