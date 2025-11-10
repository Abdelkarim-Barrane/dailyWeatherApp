import json
from logging import getLogger
from typing import List

from aiokafka import AIOKafkaProducer
from models.dto import OpenWeatherMapWeatherDataResponse
from utils.config_reader import get_config_reader


class KafkaProducerService:

    def __init__(self):
        self.__config = get_config_reader().read_kafka_producer_config()
        self.__producer: AIOKafkaProducer | None = None
        self.__logger = getLogger(self.__class__.__name__)
        self.__topic = self.__config['topic']

    async def start(self) -> None:
        if self.__producer is None:
            self.__producer = AIOKafkaProducer(
                bootstrap_servers=self.__config['bootstrapServers'],
                acks=self.__config['acks']
            )
            await self.__producer.start()

    async def stop(self) -> None:
        if self.__producer is not None:
            await self.__producer.stop()
            self.__producer = None

    @staticmethod
    def make_message_id(wd: OpenWeatherMapWeatherDataResponse) -> str:
        """Generate a unique message ID based on weather data"""

        return f"{wd.city}-{wd.country}-{wd.timestamp}"


    async def publish(self, weather_list: List[OpenWeatherMapWeatherDataResponse]) -> None:
        if self.__producer is None:
            self.__logger.error("Producer not started. Call start() before publishing messages.")
            return
        if not weather_list:
            return
        for wd in weather_list:
            key = self.make_message_id(wd).encode("utf-8")
            payload = json.dumps(wd.model_dump(), ensure_ascii=False).encode("utf-8")
            self.__logger.info(f"Sending weather data to Kafka topic {payload}")
            try:
                await self.__producer.send_and_wait(self.__topic, value=payload, key=key)
            except Exception as ex:
                self.__logger.exception("Failed to send weather message to Kafka: %s", ex)
