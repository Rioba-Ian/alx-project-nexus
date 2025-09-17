# Use a Python base image
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements.prod.txt /app/

# Development stage
FROM base AS development

# Install development dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code
COPY . .

# Expose the Django port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/swagger/ || exit 1

# Default development command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base AS production

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy the Django project code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/swagger/ || exit 1

# Create non-root user
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
USER app

# Default production command using gunicorn
CMD ["gunicorn", "jobs_board.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
