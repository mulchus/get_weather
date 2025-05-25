import requests
from django.core.management import BaseCommand
from app.models import City


def extract_cities(locations, City):
    names = []
    for location in locations:
        # в sqlite учитывается регистр при фильтрации на русском, поэтому приводим к нижнему
        # после перехода на postgres регистр не важен
        names.append(location['name'].lower())
        if location['areas']:
            names.extend(extract_cities(location['areas'], City))
    return names


class Command(BaseCommand):
    help = 'Command for fill db with locations'

    def handle(self, *args, **kwargs):
        if City.objects.count() > 10000:  # предотвращаем повторное наполнение БД при перезапуске сервера
            print('\nDatabase is already filled.')
            return
        print(f'\nStart load locations in to DB.')
        try:
            response = requests.get('https://api.hh.ru/areas')
            response.raise_for_status()
            locations = response.json()
            cities = extract_cities(locations, City)
            City.objects.bulk_create([City(name=name) for name in cities])
            print(f'Loaded {len(cities)} locations\n')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching locations: {e}\n")
