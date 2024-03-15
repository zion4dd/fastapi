cd src
start celery -A tasks worker --pool=solo --loglevel=info
timeout /t 7
start celery -A tasks flower
