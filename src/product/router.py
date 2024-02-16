from typing import List, Mapping
from fastapi import APIRouter, Depends

from product.logic import (
    add_to_cart, add_to_favorite, fin_to_brand, get_all_product,
    create_product, get_one_product, get_products_by_search
)
from product.schemas import ReadAllProduct, ReadOneProduct


router = APIRouter(
    prefix="/products",
    tags=["Product"]
)


@router.get('/{brand_id}', response_model=List[ReadAllProduct])
async def get_brand(
    brand_id: int = Depends(fin_to_brand)
):
    return brand_id


@router.get('/search', response_model=List[ReadAllProduct])
async def search_product(
    search: str = Depends(get_products_by_search)
):
    return search


@router.get('/', response_model=List[ReadAllProduct])
async def receive_all_product(
    product: list[Mapping] = Depends(get_all_product)
):
    return product


@router.get('/{product_id}', response_model=List[ReadOneProduct])
async def receive_one_product(
    product_id: int = Depends(get_one_product)
):
    return product_id


@router.post('/add')
async def post_product(
    new_product: list[Mapping] = Depends(create_product)
):
    return new_product


@router.post('/{new_product}/add_to_cart')
async def add_product_in_cart(
    new_product: list[Mapping] = Depends(add_to_cart)
):
    return new_product


@router.post('/{new_product}/add_to_favorite')
async def add_product_in_favorite(
    new_product: list[Mapping] = Depends(add_to_favorite)
):
    return new_product
