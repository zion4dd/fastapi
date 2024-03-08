cd src
start celery -A tasks worker --pool=solo --loglevel=info
timeout /t 5
start celery -A tasks flower
