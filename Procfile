web: gunicorn EducationalPortal.wsgi --log-file -
worker1: celery -A EducationalPortal worker -l info
worker2: celery -A EducationalPortal beat  -l info