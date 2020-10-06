web: gunicorn applifting.wsgi --log-file - --workers 5 --preload --timeout 10
worker: celery --app applifting.celery:app worker --beat -l info
