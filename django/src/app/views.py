import requests
from django.conf import settings
from django.shortcuts import render
from .forms import CityForm

def index(request):
    weather_data = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_api_key = settings.ENV.WEATHER_API_KEY
            weather_api_url = settings.ENV.WEATHER_API_URL
            params = {
                'q': city,
                'appid': weather_api_key,
                'units': 'metric',
                'lang': 'ru',
            }
            response = requests.get(
                weather_api_url,
                params=params,
            )
            if response.status_code == 200:
                weather_data = response.json()
            else:
                print(response.__dict__)
                weather_data = {'error': 'Невозможно получить данные о погоде.'}
    else:
        form = CityForm()

    return render(request, 'weather/index.html', {'form': form, 'weather_data': weather_data})
