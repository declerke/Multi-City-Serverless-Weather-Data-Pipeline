import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather_client import WeatherClient

class TestWeatherClient(unittest.TestCase):
    
    def setUp(self):
        self.client = WeatherClient()
    
    @patch('weather_client.urllib3.PoolManager')
    def test_get_weather_success(self, mock_pool):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = json.dumps({
            'current': {
                'temperature_2m': 20.5,
                'weather_code': 1
            }
        }).encode('utf-8')
        
        mock_http = MagicMock()
        mock_http.request.return_value = mock_response
        mock_pool.return_value = mock_http
        
        self.client.http = mock_http
        result = self.client.get_weather(0.0, 0.0)
        
        self.assertIsNotNone(result)
        self.assertIn('current', result)
    
    def test_parse_weather_data(self):
        raw_data = {
            'current': {
                'temperature_2m': 22.3,
                'relative_humidity_2m': 65,
                'weather_code': 2,
                'wind_speed_10m': 3.5,
                'time': '2026-01-15T12:00'
            }
        }
        
        parsed = self.client.parse_weather_data(raw_data)
        
        self.assertEqual(parsed['temperature'], 22.3)
        self.assertEqual(parsed['humidity'], 65)
        self.assertEqual(parsed['weather_code'], 2)
        self.assertEqual(parsed['wind_speed'], 3.5)

if __name__ == '__main__':
    unittest.main()
