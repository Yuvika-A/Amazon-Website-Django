#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput
