from django.test import TestCase, Client
from django.urls import reverse
from app.forms import CityForm

from unittest.mock import patch


class WeatherViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_weather_view_get(self):
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather.html')
        self.assertContains(response, 'Введите название города')

    def test_weather_view_post_valid_city(self):
        response = self.client.post(reverse('weather'), {'city': 'Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather.html')
        self.assertIn('weather_data', response.context)
        self.assertNotIn('error', response.context['weather_data'])

    def test_weather_view_post_invalid_city(self):
        response = self.client.post(reverse('weather'), {'city': 'InvalidCity'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather.html')
        self.assertIn('weather_data', response.context)
        self.assertIn('error', response.context['weather_data'])


class CityFormTests(TestCase):

    def test_city_form_valid(self):
        form_data = {'city': 'Moscow'}
        form = CityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form_data = {'city': ''}
        form = CityForm(data=form_data)
        self.assertFalse(form.is_valid())


class WeatherAPITests(TestCase):

    @patch('requests.get')
    def test_api_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "Moscow",
            "main": {"temp": 10},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 2}
        }

        response = self.client.post(reverse('weather'), {'city': 'Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather_data', response.context)
        self.assertEqual(response.context['weather_data']['name'], 'Moscow')
