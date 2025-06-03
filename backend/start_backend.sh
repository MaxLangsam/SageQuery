#!/bin/bash
# Start SageQuery backend
set -e

if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
fi

uvicorn api.main:app --host 0.0.0.0 --port 8000 