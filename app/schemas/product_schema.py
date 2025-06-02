from pydantic import BaseModel

from app.schemas.category_schema import CategoryIn


class ProductIn(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class ProductInBase(ProductIn):

    slug: str
    rating: float
    is_active: bool
    category: CategoryIn

    model_config = {
        "from_attributes": True
    }
