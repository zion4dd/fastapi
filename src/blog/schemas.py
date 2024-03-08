from pydantic import BaseModel

class PostAdd(BaseModel):
    text: str | None
