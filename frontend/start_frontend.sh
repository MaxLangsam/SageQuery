#!/bin/bash
# Start SageQuery frontend
set -e

if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
fi

npm install
npm run dev 