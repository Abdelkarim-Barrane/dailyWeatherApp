from logging import getLogger

import httpx
from models.dto import OpenWeatherMapGeocodingResponse, OpenWeatherMapWeatherDataResponse
from utils.config_reader import get_config_reader


class OpenWeatherMapService:

    def __init__(self):

        config = get_config_reader()
        openweather_api_config = config.read_weather_api_config()

        self.__logger = getLogger(self.__class__.__name__)
        self.__api_key = openweather_api_config['apiKey']
        self.__metric_unit = openweather_api_config['units']
        self.__base_url = openweather_api_config['urls']['base']
        self.__geo_endpoint = openweather_api_config['urls']['geoUrl']
        self.__data_endpoint = openweather_api_config['urls']['dataUrl']

    async def get_coordinates(self, city_name: str, country_code: str) -> OpenWeatherMapGeocodingResponse | None:
        """Get coordinates for a city using OpenWeatherMap Geocoding API"""
        url = f"{self.__base_url}{self.__geo_endpoint}"
        params = {
            "q": f"{city_name},{country_code}",
            "limit": 1,
            "appid": self.__api_key
        }
        try:
            async with httpx.AsyncClient() as client:

                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    self.__logger.warning(f"No coordinates found for city: {city_name}")
                    return None

                location = data[0]
                return OpenWeatherMapGeocodingResponse(**location)
        except httpx.HTTPError as e:
            self.__logger.error(f"HTTP error while getting coordinates for {city_name}: {e}")
            return None
        except Exception as e:
            self.__logger.error(f"Unexpected error while getting coordinates for {city_name}: {e}")
            return None

    async def get_weather_data(self, city: str, country: str, lat: float, lon: float) -> OpenWeatherMapWeatherDataResponse | None:
        """Get weather data using coordinates"""
        url = f"{self.__base_url}{self.__data_endpoint}"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.__api_key,
            "units": self.__metric_unit
        }
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    return None
                return OpenWeatherMapWeatherDataResponse(
                    city= city,
                    country= country,
                    latitude= data['coord']['lat'],
                    longitude= data['coord']['lon'],
                    temp= data['main']['temp'],
                    feels_like= data['main']['feels_like'],
                    temp_max= data['main']['temp_max'],
                    temp_min= data['main']['temp_min'],
                    humidity= data['main']['humidity'],
                    pressure= data['main']['pressure'],
                    wind_speed= data['wind']['speed'],
                    timestamp= data['dt']
                )
        except httpx.HTTPError as e:
            self.__logger.error(f"HTTP error while getting weather data: {e}")
            return None
        except Exception as e:
            self.__logger.error(f"Unexpected error while getting weather data: {e}")
            return None

