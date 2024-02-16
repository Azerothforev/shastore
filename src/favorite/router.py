from typing import Mapping, List
from fastapi import APIRouter, Depends

from favorite.logic import (
    downgrade_favorites_product, get_to_favorites_product)
from product.schemas import ReadAllProduct

router = APIRouter(
    prefix="/favorites",
    tags=["Favorite"]
)


@router.get('/', response_model=List[ReadAllProduct])
async def get_favorite_product(
    favorite: List[Mapping] = Depends(get_to_favorites_product),
):
    return favorite


@router.delete('/del')
async def delete_favorite_product(
    del_id_favorite: int = Depends(downgrade_favorites_product),
):
    return del_id_favorite
