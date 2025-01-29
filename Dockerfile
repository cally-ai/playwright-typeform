# Use the official Python image with Playwright preinstalled
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Playwright dependencies are installed
RUN playwright install --with-deps

# Expose the port Railway uses
ENV PORT=8080

# Start the app using Gunicorn
CMD ["gunicorn", "playwright_script:app", "--bind", "0.0.0.0:8080"]
