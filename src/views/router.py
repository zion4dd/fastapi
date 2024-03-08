from blog.router import get_all, get_post_by_id
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/views",
    tags=["Views"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(
    request: Request,
    lst=Depends(get_all),
):
    lst = [i["Post"] for i in lst]
    # i = {'Post': <blog.models.Post object at 0x0000021F55CFCE10>}
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "list": lst},
    )


@router.get("/search")
def search():
    return RedirectResponse(url="/views/search/0")


@router.get("/search/{post_id}")
def search_id(
    request: Request,
    post=Depends(get_post_by_id),
):
    if post:
        post = post["Post"]
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "post": post},
    )
