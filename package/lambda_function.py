import json
import os
from datetime import datetime
from weather_client import WeatherClient
from storage_handler import S3StorageHandler
from alert_handler import AlertHandler
from utils import get_config, validate_config

def lambda_handler(event, context):
    config = get_config()
    
    if not validate_config(config):
        return {
            'statusCode': 400,
            'body': "Invalid configuration"
        }

    cities = [
        {"name": "Nairobi", "lat": -1.2864, "lon": 36.8172},
        {"name": "Mombasa", "lat": -4.0500, "lon": 39.6667},
        {"name": "Kisumu", "lat": -0.0833, "lon": 34.7667},
        {"name": "Nakuru", "lat": -0.3000, "lon": 36.0667},
        {"name": "Eldoret", "lat": 0.5167, "lon": 35.2833}
    ]

    weather_client = WeatherClient()
    storage_handler = S3StorageHandler(config['bucket_name'])
    alert_handler = AlertHandler(config['sns_topic_arn'])
    
    processed_cities = []
    errors = []

    for city in cities:
        try:
            raw_data = weather_client.get_weather(city['lat'], city['lon'])
            
            if not raw_data:
                errors.append(f"Failed to fetch data for {city['name']}")
                continue

            parsed_data = weather_client.parse_weather_data(raw_data)
            storage_handler.save_weather_data(raw_data, city['name'])

            if alert_handler.should_alert(parsed_data['weather_code'], config['alert_threshold']):
                alert_handler.send_alert(city['name'], parsed_data)
            
            processed_cities.append(city['name'])
        except Exception as e:
            errors.append(f"Error processing {city['name']}: {str(e)}")

    status_code = 200 if not errors else 207
    return {
        'statusCode': status_code,
        'body': {
            "processed": processed_cities,
            "errors": errors
        }
    }