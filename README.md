https://github.com/zhanymkanov/fastapi-best-practices  
https://docs.pydantic.dev/latest/api/types/  
https://fastapi-users.github.io/fastapi-users/latest/  

http://localhost:8000/docs  
http://localhost:8000/redoc  


uvicorn main:app --reload  

alembic init migrations  
alembic revision --autogenerate -m "init"       # makemigrations  
alembic upgrade [head | <hash>]                 # migrate  


FastAPI-users
mkdir /auth
-models.py
-auth.py
-manager.py
-schemas.py
add routers to main.py
