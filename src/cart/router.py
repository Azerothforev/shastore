from typing import Mapping, List
from fastapi import APIRouter, Depends

from cart.logic import (
    buy_product, downgrade_carts_product, get_to_carts_product)
from product.schemas import ReadAllProduct

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get('/', response_model=List[ReadAllProduct])
async def get_favorite_product(
    favorite: List[Mapping] = Depends(get_to_carts_product),
):
    return favorite


@router.delete('/del_id_favorite/del')
async def delete_favorite_product(
    del_id_favorite: int = Depends(downgrade_carts_product),
):
    return {"status": "Товар удален из корзины."}


@router.post('/add_to_order')
async def buy_cart_product(
    product: int = Depends(buy_product),
):
    return product
