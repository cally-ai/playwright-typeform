#!/bin/bash

# Install Playwright browsers (redundant but ensures Chromium is installed)
playwright install --with-deps

# Run the application with Gunicorn
gunicorn -b 0.0.0.0:8080 playwright_script:app
