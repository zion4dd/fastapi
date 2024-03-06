from enum import Enum
from typing import Annotated, Optional

from fastapi import FastAPI, Path, Query  # Cookie, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Blog")

db = []


class Status(str, Enum):  # status.value
    low = "low"
    middle = "middle"
    high = "high"


class Item(BaseModel):
    id: Optional[int] = 0
    name: str = Field(min_length=2)
    price: float = Field(ge=0, default=0)
    is_offer: bool | None = None
    status: Status | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}", response_model=list[Item])
def read_item(item_id: int = 0):
    if item_id:
        return [item for item in db if item.id == item_id]
    return db


@app.put("/items/{item_id}")
def update_item(
    # Path-параметр всегда является обязательным, поскольку он составляет часть пути.
    item_id: Annotated[int, Path(title="Path string", ge=0)],
    item: Item,
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            alias="query",
            description="query will return in response",
            max_length=10,  # validation
            min_length=3,  # validation
            pattern="^[A-Z]",  # validation regex
            deprecated=True,
            include_in_schema=True,
        ),
    ] = None,
):
    return {"item_name": item.name, "item_id": item_id, "q": q}


@app.post("/additem")
def additem(item: Item):
    item.id = len(db) + 1
    db.append(item)
    return db[-1]


@app.exception_handler(Exception)
def exc(request, exception):
    return JSONResponse(content=jsonable_encoder({"error": exception.errors()}))
