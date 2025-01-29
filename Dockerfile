# Use Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Install Playwright browsers properly
RUN playwright install --with-deps chromium

# Expose port for Railway
EXPOSE 8080

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "playwright_script:app"]
