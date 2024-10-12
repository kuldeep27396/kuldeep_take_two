import unittest
from weather_etl import categorize_wind_speed, normalize_weather_condition, local_time
from datetime import datetime, timedelta

class TestWeatherETL(unittest.TestCase):

    def test_categorize_wind_speed(self):
        self.assertEqual(categorize_wind_speed(0.5), 'Calm')
        self.assertEqual(categorize_wind_speed(3), 'Light Air')
        self.assertEqual(categorize_wind_speed(10), 'Breeze')
        self.assertEqual(categorize_wind_speed(20), 'Gale')

    def test_normalize_weather_condition(self):
        self.assertEqual(normalize_weather_condition('few clouds'), 'cloudy')
        self.assertEqual(normalize_weather_condition('light rain'), 'rain')
        self.assertEqual(normalize_weather_condition('heavy snow'), 'snow')
        self.assertEqual(normalize_weather_condition('thunderstorm'), 'storm')
        self.assertEqual(normalize_weather_condition('clear sky'), 'clear')

    def test_local_time(self):
        utc_time = datetime(2023, 5, 1, 12, 0, 0)
        self.assertEqual(local_time('London', utc_time), utc_time)
        self.assertEqual(local_time('New York', utc_time), utc_time - timedelta(hours=4))
        self.assertEqual(local_time('Tokyo', utc_time), utc_time + timedelta(hours=9))

if __name__ == '__main__':
    unittest.main()