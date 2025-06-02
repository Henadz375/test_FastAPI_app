from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str
    parent_id: int | None

