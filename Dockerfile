FROM python:3

RUN mkdir /fastapi-app

WORKDIR /fastapi-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# docker-compose:
RUN chmod a+x docker/*.sh

# WORKDIR src

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000



# docker build . -t fastapi_app:latest

# docker run -p 1234:8000 fastapi_app

# docker ps

# docker logs <id>

# docker exec -it <cont-name> bash      # to run commands in container
