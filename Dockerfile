# Use Playwright base image (includes Chromium, Firefox, WebKit)
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Playwright browsers are installed
RUN playwright install --with-deps

# Expose the correct port
EXPOSE 8080

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "playwright_script:app"]
