FROM python:3.11-slim

# Installation de cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des fichiers du projet
COPY requirements.txt .
COPY src/ ./src/
RUN pip install --no-cache-dir -r requirements.txt

# Création des répertoires
RUN mkdir -p /app/config
RUN mkdir -p /var/log/weather-app

# Script d'entrée pour initialiser cron avec les variables d'environnement
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Préparation des logs
RUN touch /var/log/weather-app/app.log
RUN touch /var/log/cron.log

ENTRYPOINT ["/entrypoint.sh"]
