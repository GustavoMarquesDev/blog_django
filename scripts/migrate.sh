#!/bin/sh
makemigrations.sh
python manage.py migrate --no-input