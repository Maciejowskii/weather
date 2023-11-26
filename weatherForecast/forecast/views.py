import requests
from django.shortcuts import render
import os
from dotenv import load_dotenv

def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        load_dotenv()
        api_key = os.environ.get('API_KEY')


        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temperature_feel_celsius = data['main']['temp']
            temperature_celsius = data['main']["feels_like"]
            clouds = data['clouds']['all']
            clouds = int(clouds)
            rain = data['main']['humidity']
            rain = int(rain)
            main = data['weather'][0]['main']
            temperature_feel_celsius = int(temperature_feel_celsius)
            temperature_celsius = int(temperature_celsius)

            if main == 'Clear':
                cloudStatus = 1
            elif main == 'Thunderstorm':
                cloudStatus = 2
            elif main == 'Rain':
                cloudStatus = 3
            elif main == 'Snow':
                cloudStatus = 4
            elif main == "Clouds":
                cloudStatus = 5
            else:
                cloudStatus = 6

            # cloudStatus:
            #     1 - clear
            #     2 - thunderstorm
            #     3 - rainy
            #     4 - snowy
            #     5 - cloudy
            #     6 - other

            if temperature_celsius <= -10:
                feel = 'very cold'
                clothes = "comfy hoodie, don't leave the house, take a blanket, if you have an AMD processor, open the computer case"
            if temperature_celsius < 1 and temperature_celsius > -10:
                feel = 'hoarfrost'
                clothes = 'Winter Jacket'
            if temperature_celsius < 10 and temperature_celsius >= 1:
                feel = 'cold'
                clothes = 'warm jacket or hoodie'
            if temperature_celsius >= 10 and temperature_celsius < 25:
                feel = 'normal'
                clothes = 'hoodie or T-shirt'
            if temperature_celsius >= 25:
                feel = 'warm'
                clothes = 'T-shirt'
            weather_data = {
                'city': city,
                'temperature': temperature_celsius,
                'description': data['weather'][0]['description'],
                'feel': feel,
                'clothes': clothes,
                'feels_like': temperature_feel_celsius,
                # 'rain': ifRain,
                # 'clouds': ifClouds,
                'cloudStatus': cloudStatus
            }
        else:
            weather_data = None

        return render(request, 'main.html', {'weather_data': weather_data})

    return render(request, 'main.html', {'weather_data': None})