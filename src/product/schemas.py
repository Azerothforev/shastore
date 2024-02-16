from pydantic import BaseModel


class ProductCreate(BaseModel):
    price: int
    description: str
    information: str
    brand_id: int
    category_id: int
    state_id: int
    color_id: int


class ReadUser(BaseModel):
    email: str
    username: str


class ReadBrand(BaseModel):
    name: str


class ReadCategory(BaseModel):
    name: str


class ReadColor(BaseModel):
    name: str


class ReadState(BaseModel):
    name: str


class ReadAllProduct(BaseModel):
    price: int
    description: str
    information: str
    interest: int
    seller: ReadUser
    category: ReadCategory
    brand: ReadBrand


class ReadOneProduct(BaseModel):
    price: int
    description: str
    information: str
    interest: int
    seller: ReadUser
    category: ReadCategory
    brand: ReadBrand
    color: ReadColor
    state: ReadState
