# https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

# choose Transport and Stratagy
# cookie_secure=False for http protocol browser save cookie (not works for MSEdge)
cookie_transport = CookieTransport(cookie_max_age=3600*24, cookie_secure=False)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600*24)


# create a backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
