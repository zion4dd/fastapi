from time import perf_counter
from typing import Annotated, Mapping

from auth.config import current_user
from auth.models import User
from database import get_async_session
from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Request
from fastapi_cache.decorator import cache
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.celery import send_email

from .models import Post
from .schemas import PostAdd

router = APIRouter()  # dependencies - зависимости для всех эндпоинтов роутера
Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/")
@cache(expire=10)
async def get_all(
    session: Session,
    limit: int = 100,
    offset: int = 0,
    # session: AsyncSession = Depends(get_async_session),
    # session: Annotated[AsyncSession, Depends(get_async_session)]
    # 2 способа. Рекомендуется использовать версию с Annotated если возможно.
):
    a = perf_counter()
    stmt = select(Post).limit(limit).offset(offset)
    result = await session.execute(stmt)
    print(perf_counter() - a)
    return result.mappings().all()


@router.post("/")
async def add_post(
    session: Session,
    item: PostAdd,
    user: User = Depends(current_user),
):
    user_dict = item.model_dump()
    user_dict["user_id"] = user.id
    stmt = insert(Post).values(**user_dict)
    result = await session.execute(stmt)
    await session.commit()
    return {"msg": "success", "post_id": result.inserted_primary_key[0]}

    # stmt = insert(Post).values(**user_dict).returning(Post.id)  # literal_column("*")
    # return {"message": "success", "post_id": result.fetchone()[0]}


@router.delete("/del/{id}")
async def del_post(
    session: Session,
    id: int,
    user: User = Depends(current_user),
):
    stmt = delete(Post).where(Post.id >= id, Post.user_id == user.id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "success"}


@router.get("/send_email_background")
async def send_email_background(backgr: BackgroundTasks):
    "backgroun task via Fastapi background tasks - Task sleep 10 sec"

    backgr.add_task(send_email, 42)
    return {"email status": "success", "delay": "10 seconds"}


@router.get("/send_email_celery")
async def send_email_celery():
    "backgroun task via Celery - Task sleep 10 sec"

    send_email.delay(42)
    return {"email status": "success", "delay": "10 seconds"}


# dependency injection by FastAPI (может быть классом)
async def get_post(
    session: Session, post_id: int = 0, q: str = "some query"
) -> Mapping:
    print("Q:", q)
    stmt = select(Post).where(Post.id == post_id)
    post = await session.execute(stmt)
    return post.mappings().fetchone()


class PostGet:  # пример использования класса dependencies
    def __init__(self, post_id: int, q: str, session: Session):
        self.post_id = post_id
        self.q = q
        self.session = session


# Это стандартный синтаксис python и называется "type alias":
PostDep = Annotated[Mapping, Depends(get_post)]
# PostDep = Annotated[PostGet, Depends(PostGet)] OR Annotated[PostGet, Depends()]


async def print_token(fastapiusersauth: Annotated[str | None, Cookie()] = None):
    print("TOKEN:", fastapiusersauth)


class AuthGuard:
    "Callable объект передается в dependecies чтобы проверить наличие куки 'fastapiusersauth'"

    def __call__(self, request: Request):
        if "fastapiusersauth" not in request.cookies:
            raise HTTPException(
                status_code=403,
                detail="Cookie 'fastapiusersauth' not found. Login please.",
            )
        print("Cookie:", request.cookies["fastapiusersauth"])


authguard = AuthGuard()


@router.get("/{post_id}", dependencies=[Depends(print_token), Depends(authguard)])
# These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) won't be passed to your path operation function.
# async def get_post_by_id(post: Mapping = Depends(valid_post_id)):
async def get_post_by_id(post: PostDep):
    return post
