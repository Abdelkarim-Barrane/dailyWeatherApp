import asyncio
import logging

from services.processors import ProcessWeatherDataService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    process = ProcessWeatherDataService()
    await process.publish_weather_data()
    logger.info("Program finished successfully")

if __name__ == "__main__":
    asyncio.run(main())
