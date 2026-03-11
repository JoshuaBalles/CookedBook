# Use official Python image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Create data directory for persistent database
RUN mkdir -p /data

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run with uvicorn for hot reload support
# --reload enables auto-reload when code changes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Label for better organization
LABEL maintainer="CookedBook"
LABEL description="A recipe management web application"
