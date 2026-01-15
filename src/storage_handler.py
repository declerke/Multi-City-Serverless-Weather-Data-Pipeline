import boto3
import json
from datetime import datetime
from typing import Dict, Any

class S3StorageHandler:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
    
    def save_weather_data(
        self, 
        data: Dict[str, Any], 
        city: str,
        custom_timestamp: str = None
    ) -> str:
        timestamp = custom_timestamp or datetime.now().strftime("%Y-%m-%d-%H%M")
        file_key = f"weather-data/{city}/{timestamp}.json"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=json.dumps(data, indent=2),
                ContentType='application/json',
                Metadata={
                    'city': city,
                    'timestamp': timestamp,
                    'data-type': 'weather-forecast'
                }
            )
            
            print(f"Successfully saved weather data to s3://{self.bucket_name}/{file_key}")
            return file_key
            
        except Exception as e:
            print(f"Error saving to S3: {e}")
            raise
    
    def get_weather_data(self, city: str, timestamp: str) -> Dict[str, Any]:
        file_key = f"weather-data/{city}/{timestamp}.json"
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            data = json.loads(response['Body'].read().decode('utf-8'))
            return data
            
        except Exception as e:
            print(f"Error reading from S3: {e}")
            return None
    
    def list_weather_data(self, city: str, limit: int = 10) -> list:
        prefix = f"weather-data/{city}/"
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=limit
            )
            
            objects = response.get('Contents', [])
            return [obj['Key'] for obj in objects]
            
        except Exception as e:
            print(f"Error listing S3 objects: {e}")
            return []
