import pandas as pd
import json
from datetime import datetime, timedelta


# Function to read and process JSON with pandas
def process_weather_data():
    # Load the JSON data
    with open("extracted_weather_data.json", 'r') as file:
        data = json.load(file)

    # Convert JSON to DataFrame
    df = pd.json_normalize(data)

    # Perform transformations
    df['temperature_kelvin'] = df['main.temp']
    df['temperature_celsius'] = df['temperature_kelvin'] - 273.15
    df['temperature_fahrenheit'] = df['temperature_celsius'] * 9 / 5 + 32
    df['humidity'] = df['main.humidity']
    df['wind_speed'] = df['wind.speed']

    # Categorize wind speed
    df['wind_category'] = df['wind_speed'].apply(lambda speed: 'Calm' if speed < 1 else
    'Light Air' if speed < 5 else
    'Breeze' if speed < 15 else 'Gale')

    # Categorize weather conditions
    df['weather_condition'] = df['weather'].apply(lambda x: 'cloudy' if 'cloud' in x[0]['description'].lower() else
    'rain' if 'rain' in x[0]['description'].lower() or 'drizzle' in x[0]['description'].lower() else
    'snow' if 'snow' in x[0]['description'].lower() else
    'storm' if 'storm' in x[0]['description'].lower() or 'thunder' in x[0]['description'].lower() else
    'clear')

    # Convert UNIX timestamp to UTC and local times
    df['timestamp_utc'] = df['dt'].apply(lambda x: datetime.utcfromtimestamp(x))

    # Function to adjust time based on city
    def local_time(city, timestamp):
        time_offsets = {
            'London': 0,
            'New York': -14400,  # UTC-4
            'Tokyo': 32400,  # UTC+9
            'Sydney': 36000,  # UTC+10
            'Berlin': 3600  # UTC+1
        }
        return timestamp + timedelta(seconds=time_offsets.get(city, 0))

    df['timestamp_local'] = df.apply(lambda row: local_time(row['name'], row['timestamp_utc']), axis=1)

    # Save the transformed data
    df.to_csv("transformed_weather_data.csv", index=False)

    # Create daily aggregation
    df['date'] = df['timestamp_utc'].dt.date
    daily_summary = df.groupby(['name', 'date']).agg({
        'temperature_celsius': 'mean',
        'humidity': 'mean',
        'wind_speed': 'max',
        'weather_condition': lambda x: list(x)
    }).reset_index()

    daily_summary.columns = ['city', 'date', 'avg_temperature_celsius', 'avg_humidity', 'max_wind_speed',
                             'weather_conditions']

    # Save the daily summary
    daily_summary.to_csv("daily_weather_summary.csv", index=False)


if __name__ == "__main__":
    process_weather_data()
