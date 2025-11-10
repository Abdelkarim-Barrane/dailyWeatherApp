from typing import Optional

from pydantic import BaseModel


class OpenWeatherMapGeocodingResponse(BaseModel) :
    name: str
    lat: float
    lon: float
    country: str
    state: Optional[str] = None

class OpenWeatherMapWeatherDataResponse(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    temp: float
    feels_like: float
    temp_max: float
    temp_min: float
    humidity: int
    pressure: int
    wind_speed: float
    timestamp: int