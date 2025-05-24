from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather, name='weather'),
    path('api/viewed_cities', views.viewed_cities, name='viewed_cities'),
]
