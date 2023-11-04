import requests
from django.shortcuts import render
import os
from dotenv import load_dotenv

def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        load_dotenv()
        api_key = os.environ.get('API_KEY')


        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temperature_kelvin = data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            temperature_celsius = int(temperature_celsius)
            if temperature_celsius <= 10:
                feel = 'cold'
                clothes = 'warm jacket or hoodie'
            if temperature_celsius > 10 and temperature_celsius < 25:
                feel = 'normal'
                clothes = 'hoodie or T-shirt'
            if temperature_celsius > 25:
                feel = 'warm'
                clothes = 'T-shirt'
            weather_data = {
                'city': city,
                'temperature': temperature_celsius,
                'description': data['weather'][0]['description'],
                'feel': feel,
                'clothes': clothes,
            }
        else:
            weather_data = None

        return render(request, 'main.html', {'weather_data': weather_data})

    return render(request, 'main.html', {'weather_data': None})