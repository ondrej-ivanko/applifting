web: gunicorn applifting.wsgi --log-file - --preload --timeout 10
web: celery -A applifting worker --l info
web: celery -A applifting beat --l info