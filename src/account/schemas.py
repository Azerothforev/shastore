from pydantic import BaseModel


class UpdateProduct(BaseModel):
    price: int
    description: str
    information: str
    brand_id: int
    category_id: int
    state_id: int
    color_id: int
