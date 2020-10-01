from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('search', views.search),
    path('getLatLng', views.getLatLng),
]