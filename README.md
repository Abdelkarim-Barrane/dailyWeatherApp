# Daily Weather API

## Description

This project is a service that retrieves daily weather data and publishes it to a Kafka topic. It is designed to run as a scheduled task (cron job) in a containerized environment.

The architecture is orchestrated with Docker Compose and includes the following services:
-   **weather-app**: The Python application that produces the data.
-   **kafka**: The message broker for asynchronous communication.
-   **kafka-ui**: A web UI to visualize and manage Kafka topics and messages.

## Local Development Setup

Follow these steps to run the project on your local machine using Docker Compose.

### Prerequisites

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Steps
1.  **Clone the repository**

    ```bash
    git clone

2.  **Start the services**

    Use Docker Compose to build the images and start all containers in the background.

    ```bash
    docker compose up -d --build
    ```

3.  **Verify it's working**

    -   **Application Logs**: To see if the Python script is running and sending data, check the container logs. The cron job is configured to run periodically.

        ```bash
        docker compose logs -f weather-app
        ```

    -   **Kafka UI**: To view the data directly in Kafka:
        -   Open your browser and go to [http://localhost:8080](http://localhost:8080).
        -   Navigate to the `weather_data` topic (or the name configured in your `.env` file).
        -   You will be able to see the messages containing the weather data.

4.  **Stop the services**

    To stop and remove the containers, use the following command:

    ```bash
    docker-compose down
    ```
