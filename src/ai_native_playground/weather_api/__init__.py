"""Weather API module using OpenWeatherMap."""

from .main import app, WeatherResponse, ForecastResponse

__all__ = ["app", "WeatherResponse", "ForecastResponse"]