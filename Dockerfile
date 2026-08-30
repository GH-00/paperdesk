# Build stage - Python 3.12 slim Debian base image
FROM python:3.12-slim-bookworm

# Python runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Copy requirements.txt first for better layer caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user and group
RUN groupadd -r paperdesk && useradd -r -g paperdesk paperdesk

# Copy application source
COPY backend/app ./app

# Change ownership of application files to paperdesk user
RUN chown -R paperdesk:paperdesk /app

# Switch to non-root user
USER paperdesk

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=2s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()"]

# Run application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
