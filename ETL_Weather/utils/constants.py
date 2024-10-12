import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = ["London", "New York", "Tokyo", "Sydney", "Berlin"]

CITY_TIMEZONES = {
    'London': 0,
    'New York': -14400,  # UTC-4
    'Tokyo': 32400,  # UTC+9
    'Sydney': 36000,  # UTC+10
    'Berlin': 3600  # UTC+1
}