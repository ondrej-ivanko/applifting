web: gunicorn applifting.wsgi --log-file - --preload --timeout 10
worker: celery --app applifting.celery:app worker -l info
beat: celery --app applifting.celery:app beat -l info