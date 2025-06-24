#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Create admin user and get resume ID
python manage.py create_admin_user --email=admin@portfolio.com --password=admin123

# Collect static files
python manage.py collectstatic --noinput

# Final check
python manage.py check 