web: gunicorn applifting.wsgi --log-file - --preload --timeout 10
worker: celery --app applifting.celery:app worker --beat -l info
