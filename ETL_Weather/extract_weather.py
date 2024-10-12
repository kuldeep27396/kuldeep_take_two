import os

import requests
import json
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenWeatherMap API configuration
API_KEY = "1f93b831f6cf6bebfd1797a087fa1b17"
# API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of cities
CITIES = ["London", "New York", "Tokyo", "Sydney", "Berlin"]

def extract_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            data['timestamp'] = datetime.utcnow().isoformat()
            logging.info(f"Successfully fetched data for {city}")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: Error fetching data for {city}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logging.error(f"All attempts failed for {city}")
                return None

def main():
    extracted_data = []

    for city in CITIES:
        data = extract_weather_data(city)
        if data:
            extracted_data.append(data)

    if extracted_data:
        # Save the extracted data to a JSON file
        with open('extracted_weather_data.json', 'w') as f:
            json.dump(extracted_data, f, indent=2)
        logging.info(f"Successfully extracted data for {len(extracted_data)} cities and saved to extracted_weather_data.json")
    else:
        logging.error("No data was successfully extracted. Check your API key and try again.")

if __name__ == "__main__":
    main()