# Dockerfile for Flight Booking Frontend
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Your Name"
LABEL description="Flight Booking Frontend Application"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy requirements.txt FIRST for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 5000
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=2)"

# Run the Flask application
CMD ["python", "app.py"]
