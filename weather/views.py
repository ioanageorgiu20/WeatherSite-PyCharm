from django.shortcuts import render
import requests
import json
from datetime import datetime

key = "b5ad8f226b5d8e97c5522e5b3fb1da72"
url = "http://api.openweathermap.org/data/2.5/weather"


def get_weather_report(city):
    params = {
        "q": city,
        "appid": key
    }
    response = requests.get(url=url, params=params)
    return response


def get_page_context(response, city):
    return {'city_name': city,
            'temp': (response['main']['temp'] - 273.15).__round__(2),
            'weather_code': response['weather'][0]['main'],
            'wind_speed': response['wind']['speed'],
            'humidity': response['main']['humidity']}


def process_response(weather_report_response):
    response_text = weather_report_response.text
    weather_json = json.loads(response_text)
    return weather_json


def get_sunrise_sunset(city):
    params = {
        "q": city,
        "appid": key
    }
    response = requests.get(url="http://api.openweathermap.org/data/2.5/weather", params=params)
    weather_data = response.json()

    sunrise_timestamp = weather_data['sys']['sunrise']
    sunset_timestamp = weather_data['sys']['sunset']

    sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H:%M:%S')
    sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime('%H:%M:%S')

    return {'sunrise': sunrise_time, 'sunset': sunset_time}


def index(request):
    if 'city' in request.GET:
        city = request.GET['city']
        weather_report_response = get_weather_report(city)

        if weather_report_response.status_code == 200:
            sunrise_sunset_data = get_sunrise_sunset(city)
            weather_json = process_response(weather_report_response)

            context = {
                'city_name': city,
                'temp': (weather_json['main']['temp'] - 273.15).__round__(2),
                'weather_code': weather_json['weather'][0]['main'],
                'wind_speed': weather_json['wind']['speed'],
                'humidity': weather_json['main']['humidity'],
                'sunrise_time': sunrise_sunset_data['sunrise'],
                'sunset_time': sunrise_sunset_data['sunset'],
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            return render(request, 'index.html', context)
        else:
            context = {'error_message': f"Error: Unable to fetch weather data for {city}"}
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', None)