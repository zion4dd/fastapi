## Deploy
- connect VPS
- run and save .env:
    - mkdir /root/fastapi_app
    - mkdir /root/fastapi_app/nginx
    - git clone https://github.com/zion4dd/fastapi /root/fastapi_app/app
    - cp /root/fastapi_app/app/nginx.conf /root/fastapi_app/nginx/
    - nano /root/fastapi_app/.env
- run:
    - cd /root/fastapi_app/app
    - docker compose build
    - docker compose up -d

## Docs
https://github.com/zhanymkanov/fastapi-best-practices  
https://docs.pydantic.dev/latest/api/types/  
https://fastapi-users.github.io/fastapi-users/latest/  
https://docs.sqlalchemy.org/en/20/core/connections.html#result-set-api
https://github.com/long2ice/fastapi-cache

## OpenAPI
http://localhost:8000/docs  
http://localhost:8000/redoc  

## Run
cd src  
uvicorn main:app --reload  

## Alembic
- alembic init migrations  
- alembic revision --autogenerate -m "init" <i>#makemigrations</i>
- alembic upgrade [head | \<hash>] <i>#migrate</i>
- alembic downgrade -1
### alembic.ini
- uncomment line: file_template = %%(year)d_%%(month)...
- prepend_sys_path = src
- set: sqlalchemy.url = %(DB_URL)s?async_fallback=True  
<i>?async_fallback=True -to use alembic with asyncpg driver</i>

## FastAPI-users
mkdir /auth  
- config.py  
- models.py  
- manager.py  
- schemas.py  

add routers to main.py  

## FastAPI-cache
pip install fastapi-cache2[redis]  

