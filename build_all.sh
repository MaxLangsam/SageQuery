#!/bin/bash
# Build and start all SageQuery services
set -e

echo "Building backend Docker image..."
docker build -t sagequery-backend ./backend

echo "Building frontend Docker image..."
docker build -t sagequery-frontend ./frontend

echo "Starting all services with docker-compose..."
docker-compose up --build 