#!/usr/bin/env bash

python ./manage.py migrate
gunicorn applifting.wsgi --bind 0.0.0.0:8080 --workers 5