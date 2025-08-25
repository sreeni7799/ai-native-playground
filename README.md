# Weather API

A FastAPI application that fetches weather data using OpenWeatherMap OneCall 3.0 API.

## Features

- Get current weather for any city with enhanced data (UV index, feels like temperature)
- Get 8-day weather forecast for any city
- Uses geocoding to convert city names to coordinates
- Built with FastAPI and async/await
- Comprehensive test coverage with pytest

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get an API key from [OpenWeatherMap](https://openweathermap.org/api) and create a `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and add your API key:
```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## Running the Application

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Current Weather
```
GET /current?city=Kanhangad
```

Returns current weather data for the specified city.

### Weather Forecast
```
GET /forecast?city=Kanhangad
```

Returns 5-day weather forecast for the specified city.

### Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Running Tests

```bash
pytest test_main.py -v
```

## Example Usage

```bash
# Current weather
curl "http://localhost:8000/current?city=Kanhangad"

# Weather forecast
curl "http://localhost:8000/forecast?city=Kanhangad"
```