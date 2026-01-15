import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    
    @patch('lambda_function.boto3.client')
    @patch('lambda_function.urllib3.PoolManager')
    @patch.dict(os.environ, {
        'BUCKET_NAME': 'test-bucket',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789:test-topic',
        'CITY_NAME': 'TestCity',
        'LAT': '0.0',
        'LON': '0.0'
    })
    def test_lambda_handler_success(self, mock_urllib, mock_boto):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = json.dumps({
            'current': {
                'temperature_2m': 25.5,
                'weather_code': 0
            }
        }).encode('utf-8')
        
        mock_http = MagicMock()
        mock_http.request.return_value = mock_response
        mock_urllib.return_value = mock_http
        
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3
        
        result = lambda_handler({}, {})
        
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Successfully processed', result['body'])
        mock_s3.put_object.assert_called_once()
    
    @patch('lambda_function.boto3.client')
    @patch('lambda_function.urllib3.PoolManager')
    @patch.dict(os.environ, {
        'BUCKET_NAME': 'test-bucket',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789:test-topic',
        'CITY_NAME': 'TestCity',
        'LAT': '0.0',
        'LON': '0.0'
    })
    def test_lambda_handler_alert_triggered(self, mock_urllib, mock_boto):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = json.dumps({
            'current': {
                'temperature_2m': 15.0,
                'weather_code': 65
            }
        }).encode('utf-8')
        
        mock_http = MagicMock()
        mock_http.request.return_value = mock_response
        mock_urllib.return_value = mock_http
        
        mock_s3 = MagicMock()
        mock_sns = MagicMock()
        
        def boto_client_side_effect(service):
            if service == 's3':
                return mock_s3
            elif service == 'sns':
                return mock_sns
        
        mock_boto.side_effect = boto_client_side_effect
        
        result = lambda_handler({}, {})
        
        self.assertEqual(result['statusCode'], 200)
        mock_sns.publish.assert_called_once()
        
        call_args = mock_sns.publish.call_args[1]
        self.assertIn('Weather Alert', call_args['Message'])
        self.assertEqual(call_args['TopicArn'], 'arn:aws:sns:us-east-1:123456789:test-topic')

if __name__ == '__main__':
    unittest.main()