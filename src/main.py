from contextlib import asynccontextmanager

from auth.config import auth_backend, current_user, fastapi_users
from auth.models import User
from auth.schemas import UserCreate, UserRead
from blog.router import router as blog_router
from chat.router import router as chat_router
from config import REDIS_URL
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from views.router import router as views_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    "startup event"
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    "shutdown event"


app = FastAPI(title="FastAPIapp", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    blog_router,
    prefix="/blog",
    tags=["blog"],
)

app.include_router(views_router)
app.include_router(chat_router)
# prefix, tags можно определять внутри роутера или при подключении


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.exception_handler(Exception)
async def exc(request, exception):
    return JSONResponse(content=jsonable_encoder({"error": str(exception)}))


origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=[
        # Accept, Accept-Language, Content-Language и Content-Type всегда разрешены для простых CORS-запросов
        "Set-Cookie",
        "Access-Control-Request-Method",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
