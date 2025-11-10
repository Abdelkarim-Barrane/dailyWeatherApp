from logging import getLogger
from pathlib import Path
from threading import Lock
from typing import Optional

from yaml import safe_load, YAMLError


class ConfigReader:
    """A singleton class to read configuration files with reload capability."""
    _instance = None
    _lock = Lock()

    def __new__(cls, config_root_dir: str | Path ):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, config_root_dir: str | Path):
        with self._lock:
            if not self._initialized:
                self.__logger = getLogger(self.__class__.__name__)
                self.__config_root_dir = Path(config_root_dir)
                self._initialized = True

    def __read_config(self, file_name: str, key: Optional[str] = None) -> dict:
        """
        Read configuration from a YAML file.

        Args:
            file_name: Name of the YAML file to read
            key: key to extract from the configuration

        Returns:
            Configuration data. Returns that section
            of the configuration.
        """
        config = self.__read_yaml_file(self.__config_root_dir / file_name)
        return config.get(key) if key else config

    def __read_yaml_file(self, file_path: Path) -> dict:
        """Read a YAML file and return its content."""
        try:
            file_path = file_path.resolve(strict=True)
            with open(file_path, 'r', encoding='utf-8') as file:
                return safe_load(file) or {}
        except FileNotFoundError:
            self.__logger.error(f"File not found: {file_path}")
            return {}
        except YAMLError as e:
            self.__logger.error(f"YAML parsing error in {file_path}: {e}")
            return {}
        except Exception as e:
            self.__logger.error(f"Unexpected error reading {file_path}: {e}")
            return {}

    def read_cities_config(self) -> dict:
        """Read cities configuration from YAML file."""
        return self.__read_config("cities.yaml", 'countries')


    def read_weather_api_config(self) -> dict:
        """Read weather API configuration from YAML file."""
        return self.__read_config("openweathermap-endpoints.yaml")

    def read_kafka_producer_config(self) -> dict:
        """Read Kafka producer configuration from YAML file."""
        return self.__read_config("kafka-producer.yaml")

def get_config_reader(config_root_dir: str | Path = "./config/") -> ConfigReader:
    """ Factory function to create a ConfigReader instance. """
    return ConfigReader(config_root_dir)