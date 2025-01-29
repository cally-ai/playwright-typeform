# Use Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN npx playwright install --with-deps

# Expose port for Railway
EXPOSE 8080

# Start the application
CMD ["bash", "start.sh"]
