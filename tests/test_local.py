import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather_client import WeatherClient
from utils import get_weather_severity

def test_local(lat, lon, city):
    print("=" * 60)
    print(f"Testing Weather API for {city}")
    print(f"Coordinates: {lat}, {lon}")
    print("=" * 60)
    
    client = WeatherClient()
    
    print(f"\n[{datetime.now()}] Fetching weather data...")
    data = client.get_weather(lat, lon)
    
    if not data:
        print("❌ Failed to fetch weather data")
        return False
    
    print("✅ Weather data fetched successfully")
    
    parsed = client.parse_weather_data(data)
    
    print("\n📊 Current Weather:")
    print(f"  Temperature: {parsed['temperature']}°C")
    print(f"  Humidity: {parsed['humidity']}%")
    print(f"  Weather Code: {parsed['weather_code']}")
    print(f"  Wind Speed: {parsed['wind_speed']} m/s")
    print(f"  Timestamp: {parsed['timestamp']}")
    
    severity = get_weather_severity(parsed['weather_code'])
    print(f"  Severity: {severity.upper()}")
    
    if parsed['weather_code'] >= 51:
        print("\n⚠️  ALERT: Weather conditions warrant notification")
    else:
        print("\n✅ Weather conditions are normal")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test weather API locally')
    parser.add_argument('--lat', type=float, default=-1.286389, help='Latitude')
    parser.add_argument('--lon', type=float, default=36.817223, help='Longitude')
    parser.add_argument('--city', type=str, default='Nairobi', help='City name')
    
    args = parser.parse_args()
    
    success = test_local(args.lat, args.lon, args.city)
    sys.exit(0 if success else 1)
