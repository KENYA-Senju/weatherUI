import requests
from utils import c_to_f, kmh_to_mph
from config import config

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    res = requests.get(url).json()

    if "results" not in res:
        return None, None

    r = res["results"][0]
    return r["latitude"], r["longitude"]


def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    return requests.get(url).json()


def update_forecast(temp, windspeed, winddir):
    root = config.window

    root.temp_label.config(text=f"{c_to_f(temp)} °F")
    root.wind_label.config(text=f"{kmh_to_mph(windspeed)} mph")
    root.dir_label.config(text=f"{winddir}°")


def display_weather(city, data):
    current = data["current_weather"]

    print(f"\nWeather for {city}")
    print(f"Temp: {c_to_f(current['temperature'])}°F")

    update_forecast(
        current["temperature"],
        current["windspeed"],
        current["winddirection"]
    )