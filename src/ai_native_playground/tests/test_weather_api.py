import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import os
from main import app

client = TestClient(app)

@pytest.fixture
def mock_geocoding_response():
    return [
        {
            "name": "Kanhangad",
            "lat": 12.31,
            "lon": 75.1
        }
    ]

@pytest.fixture
def mock_onecall_current_response():
    return {
        "current": {
            "temp": 28.5,
            "feels_like": 30.2,
            "humidity": 75,
            "pressure": 1013,
            "uvi": 6.5,
            "wind_speed": 5.2,
            "weather": [
                {
                    "description": "partly cloudy"
                }
            ]
        }
    }

@pytest.fixture
def mock_onecall_forecast_response():
    return {
        "daily": [
            {
                "dt": 1704110400,
                "temp": {
                    "day": 29.0
                },
                "feels_like": {
                    "day": 31.5
                },
                "humidity": 70,
                "pressure": 1015,
                "wind_speed": 4.2,
                "weather": [
                    {
                        "description": "sunny"
                    }
                ]
            },
            {
                "dt": 1704196800,
                "temp": {
                    "day": 31.5
                },
                "feels_like": {
                    "day": 34.0
                },
                "humidity": 65,
                "pressure": 1012,
                "wind_speed": 3.8,
                "weather": [
                    {
                        "description": "clear sky"
                    }
                ]
            }
        ]
    }

class TestWeatherAPI:
    
    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_api_key"})
    @patch("httpx.AsyncClient.get")
    def test_current_weather_success(self, mock_get, mock_geocoding_response, mock_onecall_current_response):
        mock_response = AsyncMock()
        mock_get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [
            mock_response,  # geocoding call
            mock_response   # onecall call
        ]
        mock_response.json.side_effect = [
            mock_geocoding_response,
            mock_onecall_current_response
        ]
        
        response = client.get("/current?city=Kanhangad")
        
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Kanhangad"
        assert data["lat"] == 12.31
        assert data["lon"] == 75.1
        assert data["temperature"] == 28.5
        assert data["feels_like"] == 30.2
        assert data["description"] == "partly cloudy"
        assert data["humidity"] == 75
        assert data["pressure"] == 1013
        assert data["wind_speed"] == 5.2
        assert data["uv_index"] == 6.5

    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_api_key"})
    @patch("httpx.AsyncClient.get")
    def test_forecast_weather_success(self, mock_get, mock_geocoding_response, mock_onecall_forecast_response):
        mock_response = AsyncMock()
        mock_get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [
            mock_response,  # geocoding call
            mock_response   # onecall call
        ]
        mock_response.json.side_effect = [
            mock_geocoding_response,
            mock_onecall_forecast_response
        ]
        
        response = client.get("/forecast?city=Kanhangad")
        
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Kanhangad"
        assert data["lat"] == 12.31
        assert data["lon"] == 75.1
        assert len(data["forecast"]) == 2
        assert data["forecast"][0]["temperature"] == 29.0
        assert data["forecast"][0]["feels_like"] == 31.5
        assert data["forecast"][0]["description"] == "sunny"
        assert data["forecast"][0]["pressure"] == 1015
        assert data["forecast"][0]["wind_speed"] == 4.2

    def test_current_weather_missing_city(self):
        response = client.get("/current")
        assert response.status_code == 422

    def test_forecast_weather_missing_city(self):
        response = client.get("/forecast")
        assert response.status_code == 422

    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": ""})
    def test_missing_api_key(self):
        response = client.get("/current?city=Kanhangad")
        assert response.status_code == 500
        assert "API key not configured" in response.json()["detail"]

    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_api_key"})
    @patch("httpx.AsyncClient.get")
    def test_city_not_found(self, mock_get):
        mock_response = AsyncMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = client.get("/current?city=InvalidCity")
        assert response.status_code == 404
        assert "City not found" in response.json()["detail"]

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Weather API" in response.json()["message"]