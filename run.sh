#!/bin/bash

echo "---------------------------------------------------"
echo " Air Quality Index – Full Stack App"
echo " Starting Backend + Frontend + Redis via Docker..."
echo "---------------------------------------------------"

# Path to backend .env
ENV_FILE="./backend/.env"

# Check for backend/.env
if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: backend/.env file not found!"
  echo "Create backend/.env with:"
  echo "OPENWEATHER_API_KEY=your_api_key_here"
  exit 1
fi

echo "Loading environment variables from backend/.env"

# Load .env safely
set -a
while IFS='=' read -r key value || [ -n "$key" ]; do
  # Skip comments & empty lines
  if [[ "$key" =~ ^# ]] || [[ -z "$key" ]]; then
    continue
  fi

  # Remove Windows CRLF if present
  value=$(echo "$value" | tr -d '\r')

  export "$key=$value"
done < "$ENV_FILE"
set +a

docker compose up --build
