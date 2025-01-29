#!/bin/bash

# Install Playwright dependencies
playwright install

# Start the app using Gunicorn
gunicorn playwright_script:app --bind 0.0.0.0:$PORT