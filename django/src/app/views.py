import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from app.forms import CityForm
from app.models import City
from django.views import View


def weather(request):
    weather_data = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city'].strip().lower()
            weather_api_key = settings.ENV.WEATHER_API_KEY
            weather_api_url = settings.ENV.WEATHER_API_URL
            params = {
                'q': city,
                'appid': weather_api_key,
                'units': 'metric',
                'lang': 'ru',
            }
            try:
                response = requests.get(
                    weather_api_url,
                    params=params,
                )
                response.raise_for_status()

                weather_data = response.json()
                if not 'cities' in request.session:
                    request.session['cities'] = {}
                if not city in request.session['cities']:
                    request.session['cities'].update({city: 1})
                    request.session.modified = True
                else:
                    request.session['cities'][city] += 1
                    request.session.modified = True

                request.session['last_city'] = city

            except requests.exceptions.HTTPError:
                weather_data = {'error': 'Невозможно получить данные о погоде.'}
    else:
        form = CityForm(
            initial={
                'city': request.session.get('last_city', None).title()
                if request.session.get('last_city', None) else ''}
        )

    return render(request, 'weather/weather.html', {'form': form, 'weather_data': weather_data})


def viewed_cities(request):
    return JsonResponse(request.session.get('cities', {}))


class CityAutocomplete(View):
    def get(self, request):
        query = request.GET.get('term', '')
        cities = set(City.objects.filter(name__istartswith=query.lower()).values_list('name', flat=True))
        cities = [city.split('(')[0] for city in cities]  # убираем из названий инфо о регионе
        return JsonResponse(cities, safe=False)
