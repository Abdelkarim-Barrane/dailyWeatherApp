#!/bin/bash

wait_for_kafka() {
    echo "Waiting for Kafka to be ready..."
    sleep 10
}

apt-get update && apt-get install -y netcat-openbsd

printenv | grep -v "^_" > /etc/environment

wait_for_kafka

echo "* * * * * root cd /app && /usr/local/bin/python /app/src/main.py >> /var/log/weather-app/app.log 2>&1" > /etc/cron.d/weather-task

chmod 0644 /etc/cron.d/weather-task

crontab /etc/cron.d/weather-task

service cron start

cd /app && /usr/local/bin/python /app/src/main.py

tail -f /var/log/weather-app/app.log /var/log/cron.log
