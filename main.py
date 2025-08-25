import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Weather API", description="Weather data from OpenWeatherMap", version="1.0.0")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
ONECALL_BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0"

class WeatherResponse(BaseModel):
    city: str
    lat: float
    lon: float
    temperature: float
    feels_like: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    uv_index: float

class ForecastItem(BaseModel):
    datetime: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float

class ForecastResponse(BaseModel):
    city: str
    lat: float
    lon: float
    forecast: List[ForecastItem]

async def get_coordinates(city: str) -> tuple[float, float]:
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    params = {
        "q": city,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{GEOCODING_BASE_URL}/direct", params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise HTTPException(status_code=404, detail="City not found")
            
            return data[0]["lat"], data[0]["lon"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="City not found")
            raise HTTPException(status_code=500, detail=f"Geocoding API error: {e.response.status_code}")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Failed to connect to geocoding service")

async def fetch_onecall_data(lat: float, lon: float, exclude: str = "") -> Dict[str, Any]:
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    if exclude:
        params["exclude"] = exclude
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ONECALL_BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Weather API error: {e.response.status_code}")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Failed to connect to weather service")

@app.get("/current", response_model=WeatherResponse)
async def get_current_weather(city: str = Query(..., description="City name")):
    lat, lon = await get_coordinates(city)
    data = await fetch_onecall_data(lat, lon, exclude="minutely,hourly,daily,alerts")
    
    current = data["current"]
    
    return WeatherResponse(
        city=city,
        lat=lat,
        lon=lon,
        temperature=current["temp"],
        feels_like=current["feels_like"],
        description=current["weather"][0]["description"],
        humidity=current["humidity"],
        pressure=current["pressure"],
        wind_speed=current["wind_speed"],
        uv_index=current["uvi"]
    )

@app.get("/forecast", response_model=ForecastResponse)
async def get_weather_forecast(city: str = Query(..., description="City name")):
    lat, lon = await get_coordinates(city)
    data = await fetch_onecall_data(lat, lon, exclude="minutely,current,alerts")
    
    forecast_items = []
    for item in data["daily"]:
        from datetime import datetime
        dt_str = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        
        forecast_items.append(ForecastItem(
            datetime=dt_str,
            temperature=item["temp"]["day"],
            feels_like=item["feels_like"]["day"],
            description=item["weather"][0]["description"],
            humidity=item["humidity"],
            pressure=item["pressure"],
            wind_speed=item["wind_speed"]
        ))
    
    return ForecastResponse(
        city=city,
        lat=lat,
        lon=lon,
        forecast=forecast_items
    )

@app.get("/")
async def root():
    return {"message": "Weather API - Use /current?city=<city_name> or /forecast?city=<city_name>"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)