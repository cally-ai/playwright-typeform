#!/bin/bash

# Install missing Playwright dependencies
npx playwright install --with-deps

# Set Playwright to use the system-installed Chromium
export PLAYWRIGHT_BROWSERS_PATH=0

# Start the Flask app using Gunicorn
gunicorn playwright_script:app --bind 0.0.0.0:$PORT
