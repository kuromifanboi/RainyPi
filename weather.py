import requests
import json

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(latitude, longitude):
    # Build the request URL with the provided coordinates and API key
    url = f"{BASE_URL}?lat={latitude}&lon={longitude}&appid={API_KEY}"

    # Send the request to OpenWeatherMap API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract relevant weather information
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"]

        # Return the extracted weather data
        return temperature, humidity, weather_description
    else:
        print("Failed to retrieve weather data.")
        return None
