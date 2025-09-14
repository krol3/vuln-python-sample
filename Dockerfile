# Use Python 3.11 slim image as base
# python Python 3.7: reached its End of Life in June 2023 and is no longer maintained or updated.
# FROM python:3.11-slim
FROM python:3.7-slim
# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 curl \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt content
# RUN echo "Flask==2.3.3" > requirements.txt
RUN echo "Flask==2.0.1" > requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create a non-root user for security (though the app itself is intentionally vulnerable)
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
#USER appuser
USER root

# Expose port
EXPOSE 50005

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50005/ || exit 1

# Add labels
LABEL maintainer="security-demo"
LABEL description="Educational SQL injection vulnerability demonstration"
LABEL version="1.0"

# Run the application
CMD ["python", "app.py"]