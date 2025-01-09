import pytest
from unittest.mock import patch, MagicMock
from weather_dashboard import WeatherDashboard

@patch('weather_dashboard.requests.get')
def test_fetch_weather(mock_get):
    # Mock the JSON data returned by requests.get
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 70, "feels_like": 68, "humidity": 40},
        "weather": [{"description": "clear sky"}]
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    dashboard = WeatherDashboard()
    data = dashboard.fetch_weather("TestCity")
    assert data is not None
    assert data['main']['temp'] == 70
    assert data['weather'][0]['description'] == "clear sky"

@patch('weather_dashboard.boto3.client')
def test_save_to_s3(mock_boto_client):
    # Mock S3 put_object
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    dashboard = WeatherDashboard()
    weather_data = {
        'main': {'temp': 70, 'feels_like': 68, 'humidity': 40},
        'weather': [{'description': 'clear sky'}],
        'timestamp': '20250101-100000'
    }
    city = "TestCity"

    success = dashboard.save_to_s3(weather_data, city)
    mock_s3.put_object.assert_called_once()
    assert success is True
