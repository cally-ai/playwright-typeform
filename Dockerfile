# Use Playwright’s official Python image
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Force Playwright to install its browsers
RUN playwright install --with-deps

# Expose Railway's default port
ENV PORT=8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "playwright_script:app", "--bind", "0.0.0.0:8080"]
