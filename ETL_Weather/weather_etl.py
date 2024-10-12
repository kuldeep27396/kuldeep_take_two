import requests
import time
import logging
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any, TypedDict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ETL_Weather.utils.constants import API_KEY, BASE_URL, CITY_TIMEZONES, CITIES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WeatherData(TypedDict):
    main: Dict[str, float]
    wind: Dict[str, float]
    weather: List[Dict[str, str]]
    name: str
    timestamp: str


def validate_weather_data(data: Dict[str, Any]) -> bool:
    """
    Validate the structure of the weather data.

    Args:
        data (Dict[str, Any]): Weather data to validate

    Returns:
        bool: True if data is valid, False otherwise
    """
    required_fields = ['main', 'wind', 'weather', 'name']
    return all(field in data for field in required_fields)


def extract_weather_data(city: str) -> Optional[WeatherData]:
    """
    Extract weather data for a given city from OpenWeatherMap API.

    Args:
        city (str): Name of the city

    Returns:
        Optional[WeatherData]: Weather data for the city, or None if extraction failed
    """
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
            if validate_weather_data(data):
                data['timestamp'] = datetime.utcnow().isoformat()
                logging.info(f"Successfully fetched data for {city}")
                return data
            else:
                logging.error(f"Invalid data format for {city}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: Error fetching data for {city}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logging.error(f"All attempts failed for {city}")
                return None


def categorize_wind_speed(speed: float) -> str:
    """
    Categorize wind speed based on given thresholds.

    Args:
        speed (float): Wind speed in m/s

    Returns:
        str: Wind speed category
    """
    if speed < 1:
        return 'Calm'
    elif speed < 5:
        return 'Light Air'
    elif speed < 15:
        return 'Breeze'
    else:
        return 'Gale'


def normalize_weather_condition(condition: str) -> str:
    """
    Normalize weather condition to standard categories.

    Args:
        condition (str): Original weather condition

    Returns:
        str: Normalized weather condition
    """
    condition = condition.lower()
    if 'cloud' in condition:
        return 'cloudy'
    elif 'rain' in condition or 'drizzle' in condition:
        return 'rain'
    elif 'snow' in condition:
        return 'snow'
    elif 'storm' in condition or 'thunder' in condition:
        return 'storm'
    else:
        return 'clear'


def local_time(city: str, timestamp: datetime) -> datetime:
    """
    Convert UTC time to local time for a given city.

    Args:
        city (str): Name of the city
        timestamp (datetime): UTC timestamp

    Returns:
        datetime: Local timestamp for the city
    """
    offset = CITY_TIMEZONES.get(city, 0)
    return timestamp + timedelta(seconds=offset)


def transform_weather_data(data: List[WeatherData]) -> pd.DataFrame:
    """
    Transform raw weather data into a structured DataFrame.

    Args:
        data (List[WeatherData]): List of raw weather data dictionaries

    Returns:
        pd.DataFrame: Transformed weather data
    """
    df = pd.json_normalize(data)

    df['temperature_kelvin'] = df['main.temp'] + 273.15
    df['temperature_celsius'] = df['main.temp']
    df['temperature_fahrenheit'] = df['temperature_celsius'] * 9 / 5 + 32
    df['humidity'] = df['main.humidity']
    df['wind_speed'] = df['wind.speed']
    df['wind_category'] = df['wind_speed'].apply(categorize_wind_speed)
    df['weather_condition'] = df['weather'].apply(lambda x: normalize_weather_condition(x[0]['description']))
    df['timestamp_utc'] = pd.to_datetime(df['timestamp'])
    df['timestamp_local'] = df.apply(lambda row: local_time(row['name'], row['timestamp_utc']), axis=1)

    return df[['name', 'timestamp_utc', 'timestamp_local', 'temperature_kelvin', 'temperature_celsius',
               'temperature_fahrenheit', 'humidity', 'wind_speed', 'wind_category', 'weather_condition']]


def aggregate_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate weather data on a daily basis.

    Args:
        df (pd.DataFrame): Transformed weather data

    Returns:
        pd.DataFrame: Daily aggregated weather data
    """
    df['date'] = df['timestamp_utc'].dt.date
    daily_summary = df.groupby(['name', 'date']).agg({
        'temperature_celsius': 'mean',
        'humidity': 'mean',
        'wind_speed': 'max',
        'weather_condition': lambda x: x.value_counts().to_dict()
    }).reset_index()

    daily_summary.columns = ['city', 'date', 'avg_temperature_celsius', 'avg_humidity', 'max_wind_speed',
                             'weather_conditions']
    return daily_summary


def main():
    extracted_data: List[WeatherData] = []
    #can be handled with stage json save for big files

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_city = {executor.submit(extract_weather_data, city): city for city in CITIES}
        for future in as_completed(future_to_city):
            city = future_to_city[future]
            try:
                data = future.result()
                if data:
                    extracted_data.append(data)
            except Exception as exc:
                logging.error(f'{city} generated an exception: {exc}')

    if extracted_data:
        try:
            # Transform data
            df_transformed = transform_weather_data(extracted_data)
            df_daily = aggregate_daily_data(df_transformed)

            # Save the transformed data
            df_transformed.to_csv("transformed_weather_data.csv", index=False)
            df_daily.to_csv("daily_weather_summary.csv", index=False)

            logging.info(f"Successfully processed data for {len(extracted_data)} cities and saved to CSV files.")
        except Exception as e:
            logging.error(f"An error occurred during data transformation or saving: {e}")
    else:
        logging.error("No data was successfully extracted. Check your API key and try again.")


if __name__ == "__main__":
    main()