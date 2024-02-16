from typing import Mapping
from fastapi import APIRouter, Depends

from account.logic import (
    delete_product, get_order_product, get_sales_product,
    get_user_product, update_user_product
)
from auth.schemas import UserRead
from product.schemas import ReadAllProduct


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)


@router.get('/profile', response_model=list[UserRead])
async def get_my_profile(
    user: Mapping = Depends(get_user_product)
):
    return user


@router.get('/products', response_model=list[ReadAllProduct])
async def my_products(
    products: list[Mapping] = Depends(get_user_product)
):
    return products


@router.get('/orders', response_model=list[ReadAllProduct])
async def get_user_orders(
    orders: int = Depends(get_order_product)
):
    return orders


@router.get('/sales', response_model=list[ReadAllProduct])
async def get_user_sales(
    orders: int = Depends(get_sales_product)
):
    return orders


@router.delete('/{product_id}/remove')
async def remove_from_publication(
    product_id: int = Depends(delete_product)
):
    return product_id


@router.put('/{product_id}/update')
async def up_product(
    product_id: int = Depends(update_user_product)
):
    return product_id
