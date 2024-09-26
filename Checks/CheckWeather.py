import requests
from APIs.apikeyofweather import apikey



def get_weather(city="Nagpur"):
    """Fetches the current weather from OpenWeatherMap API and returns the weather info along with the city name."""

    # I have set my API in APIs folder with a python file with apikey as a variable which has the openweathermap API Key
    # Add your own API by creating a variable here and replace the apikey variable to your own variable which has your API
    api_key = apikey  # API key  here replace the apikey variable to the variable that has you API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"


    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather_data = data["main"]
        temperature = weather_data["temp"]
        humidity = weather_data["humidity"]
        weather_desc = data["weather"][0]["description"]
        location_name = data["name"]  # This gives the exact name of the location from the API

        return f"Location: {location_name}\nTemp: {temperature}°C\nHumidity: {humidity}%\nCondition: {weather_desc.capitalize()}"
    else:
        return "City Not Found"
