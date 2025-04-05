import requests

def get_weather_data(location: str) -> str:
    api_key = "8d2983db0b74ee8e69fa137c469bf974"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"{temperature}°C."
    else:
        return f"Could not fetch weather data for {location}."
