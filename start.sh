#!/bin/bash

# Install missing Playwright dependencies (only if needed)
npx playwright install --with-deps

# Set Playwright to use its built-in Chromium
export PLAYWRIGHT_BROWSERS_PATH=0

# Ensure the $PORT variable is set (default to 8080 if not set by Railway)
PORT=${PORT:-8080}

# Start the Flask app using Gunicorn with proper worker management
exec gunicorn --workers=1 --threads=4 --timeout=0 -b 0.0.0.0:$PORT playwright_script:app
