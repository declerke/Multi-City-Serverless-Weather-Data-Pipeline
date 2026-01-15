import boto3
from typing import Dict, Any

class AlertHandler:
    WEATHER_CODE_DESCRIPTIONS = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    def __init__(self, sns_topic_arn: str):
        self.sns_topic_arn = sns_topic_arn
        self.sns_client = boto3.client('sns')
    
    def should_alert(self, weather_code: int, threshold: int = 51) -> bool:
        return weather_code >= threshold
    
    def get_weather_description(self, weather_code: int) -> str:
        return self.WEATHER_CODE_DESCRIPTIONS.get(
            weather_code, 
            f"Unknown condition (code {weather_code})"
        )
    
    def send_alert(
        self, 
        city: str, 
        weather_data: Dict[str, Any],
        custom_message: str = None
    ) -> bool:
        weather_code = weather_data.get('weather_code')
        temperature = weather_data.get('temperature')
        humidity = weather_data.get('humidity')
        timestamp = weather_data.get('timestamp')
        
        description = self.get_weather_description(weather_code)
        
        if custom_message:
            message = custom_message
        else:
            message = f"""
🌦️ Weather Alert for {city}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Condition: {description}
🌡️  Temperature: {temperature}°C
💧 Humidity: {humidity}%
🔢 Weather Code: {weather_code}
🕐 Time: {timestamp}

This is an automated alert from your AWS Weather System.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """.strip()
        
        try:
            response = self.sns_client.publish(
                TopicArn=self.sns_topic_arn,
                Message=message,
                Subject=f"⚠️ Weather Alert: {city}",
                MessageAttributes={
                    'city': {'DataType': 'String', 'StringValue': city},
                    'weather_code': {'DataType': 'Number', 'StringValue': str(weather_code)},
                    'alert_type': {'DataType': 'String', 'StringValue': 'weather-alert'}
                }
            )
            
            print(f"Alert sent successfully. Message ID: {response['MessageId']}")
            return True
            
        except Exception as e:
            print(f"Error sending SNS alert: {e}")
            return False