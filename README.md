# kuldeep_take_two

## Requirements

- Python 3.12
- `requests`
- `pandas`

You can install the required packages using:

```
pip install requests pandas
```

## Setup

1. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).
2. Set the API key as an environment variable (This is setup from Github Secrets):
   ```
   set OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

Run the main ETL script:

```
python weather_etl.py
```

This will:
1. Extract weather data for London, New York, Tokyo, Sydney, and Berlin.
2. Transform the data (convert temperatures, categorize wind speed, normalize weather conditions, etc.).
3. Load the data into two CSV files: `transformed_weather_data.csv` and `daily_weather_summary.csv`.

## Running Tests

To run the unit tests:

```
python -m unittest test_weather_etl.py
```

## Assumptions and Edge Cases

1. **Time Zones**: The script uses fixed offsets for time zones and doesn't account for daylight saving time changes. For production use, consider using a more robust time zone handling library like `pytz`.

2. **API Rate Limits**: The script implements a simple exponential backoff strategy for API requests. Adjust the `max_retries` and `retry_delay` variables if needed.

3. **Large Data Handling**: We will use pySpark if lots of data is coming. With dataproc we can easily handle Tb's of data.
