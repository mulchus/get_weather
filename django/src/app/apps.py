from django.apps import AppConfig
import requests


def extract_cities(locations, City):
    names = []
    for location in locations:
        # в sqlite учитывается регистр при фильтрации на русском, поэтому приводим к нижнему
        # после перехода на postgres регистр не важен
        names.append(location['name'].lower())
        if location['areas']:
            names.extend(extract_cities(location['areas'], City))
    return names


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from app.models import City
        if City.objects.count() > 10000:  # предотвращаем повторное наполнение БД при перезапуске сервера
            return
        try:
            response = requests.get('https://api.hh.ru/areas')
            response.raise_for_status()
            locations = response.json()
            cities = extract_cities(locations, City)
            City.objects.bulk_create([City(name=name) for name in cities])
            print(f'Load {len(cities)} locations')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching locations: {e}")
