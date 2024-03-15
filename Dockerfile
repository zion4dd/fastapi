FROM python:3

RUN mkdir /fastapi-app

WORKDIR /fastapi-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# docker-compose:
RUN chmod a+x scripts/*.sh

# WORKDIR src

# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000



# docker build -t fastapi_app .

# docker run --name fastapi_cont --rm -p 1234:8000 fastapi_app

# docker ps

# docker logs fastapi_cont -f

# docker exec -it fastapi_cont bash      # to run commands in container
