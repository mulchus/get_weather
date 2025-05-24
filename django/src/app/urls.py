from django.urls import path
from app import views

urlpatterns = [
    path('', views.weather, name='weather'),
    path('api/viewed_cities', views.viewed_cities, name='viewed_cities'),
    path('city_autocomplete', views.CityAutocomplete.as_view(), name='city_autocomplete'),
]
