import urllib3
import json
from typing import Dict, Any, Optional

class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.http = urllib3.PoolManager()
    
    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        url = (
            f"{self.BASE_URL}"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            f"&wind_speed_unit=ms"
            f"&timezone=auto"
        )
        
        try:
            response = self.http.request('GET', url)
            
            if response.status != 200:
                print(f"API returned status {response.status}")
                return None
            
            data = json.loads(response.data.decode('utf-8'))
            return data
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def parse_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        current = data.get('current', {})
        
        return {
            'temperature': current.get('temperature_2m'),
            'humidity': current.get('relative_humidity_2m'),
            'weather_code': current.get('weather_code'),
            'wind_speed': current.get('wind_speed_10m'),
            'timestamp': current.get('time'),
            'raw_data': data
        }