import os
from typing import Dict, Any
from datetime import datetime

def get_config() -> Dict[str, Any]:
    return {
        'lat': float(os.environ.get('LAT', '-1.286389')),
        'lon': float(os.environ.get('LON', '36.817223')),
        'city': os.environ.get('CITY_NAME', 'Nairobi'),
        'bucket_name': os.environ.get('BUCKET_NAME'),
        'sns_topic_arn': os.environ.get('SNS_TOPIC_ARN'),
        'alert_threshold': int(os.environ.get('ALERT_THRESHOLD', '51'))
    }

def validate_config(config: Dict[str, Any]) -> bool:
    required_keys = ['bucket_name', 'sns_topic_arn']
    missing_keys = [key for key in required_keys if not config.get(key)]
    
    if missing_keys:
        print(f"Missing required configuration: {', '.join(missing_keys)}")
        return False
    
    return True

def format_timestamp(dt: datetime = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d-%H%M")

def parse_timestamp(timestamp_str: str) -> datetime:
    return datetime.strptime(timestamp_str, "%Y-%m-%d-%H%M")

def get_weather_severity(weather_code: int) -> str:
    if weather_code == 0:
        return "clear"
    elif weather_code <= 3:
        return "partly_cloudy"
    elif weather_code <= 48:
        return "fog"
    elif weather_code <= 67:
        return "rain"
    elif weather_code <= 77:
        return "snow"
    elif weather_code <= 82:
        return "showers"
    elif weather_code <= 99:
        return "thunderstorm"
    else:
        return "unknown"
