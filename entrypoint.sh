#!/bin/bash
set -e

# Create static and media directories if they don't exist
mkdir -p /app/staticfiles
mkdir -p /app/mediafiles

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Determine environment (development vs production)
if [[ "$DJANGO_SETTINGS_MODULE" == *".prod"* ]] || [[ "$DEBUG" == "0" ]]; then
  echo "Running in production mode"

  # Collect static files (required for production)
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "Running in development mode"

  # In development, we don't need to collect static files
  # as Django's development server serves them automatically
  echo "Static file collection skipped in development mode"
fi

# Execute the command passed to docker
echo "Starting the application..."
exec "$@"
