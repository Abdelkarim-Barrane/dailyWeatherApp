from logging import getLogger
from typing import List

from models.dto import OpenWeatherMapWeatherDataResponse
from services.kafka_producer import KafkaProducerService
from services.openweathermap import OpenWeatherMapService
from utils.config_reader import get_config_reader


class ProcessWeatherDataService:

    def __init__(self):
        self.__config_reader = get_config_reader()
        self.__weather_service  = OpenWeatherMapService()
        self.__logger = getLogger(self.__class__.__name__)

    async def process_weather_data(self) -> List[OpenWeatherMapWeatherDataResponse]:
        config = self.__config_reader.read_cities_config()
        weather_data_list: List[OpenWeatherMapWeatherDataResponse] = []
        self.__logger.info(f"Getting coordinates")
        for country in config:
            for city in country['cities']:
                coordinates = await self.__weather_service.get_coordinates(city, country['code'])
                if coordinates:
                    weather_data = await self.__weather_service.get_weather_data(city,country['name'],coordinates.lat, coordinates.lon)
                    if weather_data:
                        weather_data_list.append(weather_data)
                    else:
                        self.__logger.warning(f"Weather data not found for {city}, {country['name']}")
                else:
                    self.__logger.warning(f"Coordinates not found for {city}, {country['name']}")
            self.__logger.info(f"Weather data for {country['name']} retrieved")
        self.__logger.info(f"Getting weather data")

        return weather_data_list

    async def publish_weather_data(self) -> None:

        weather_list = await self.process_weather_data()
        if not weather_list:
            self.__logger.info("No weather data to publish")
            return

        kafka_producer_config = KafkaProducerService()
        await kafka_producer_config.start()
        await kafka_producer_config.publish(weather_list)
        await kafka_producer_config.stop()
        self.__logger.info("Weather data published to Kafka")
