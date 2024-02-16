from fastapi import Depends, HTTPException
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.models import Favorite, Product, Cart


async def validate_product(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(and_(
            Product.id == product_id,
            Product.status == 0)
        )
    )
    result = await session.execute(query)
    product = result.scalar()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Данный продукт был куплен или недоступен."
        )
    return product


async def validate_cart(
    product_id: int = Depends(validate_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Cart).
        where(Cart.user_id == user.id)
    )
    result = await session.execute(query)
    val = result.scalar()
    if val:
        raise HTTPException(
            status_code=401,
            detail="Данный продукт Уже добавле в вашу корзину."
        )
    return product_id


async def validate_favorite(
    product: int = Depends(validate_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Favorite).
        where(
            and_(Favorite.user_id == user.id,
                 Favorite.product_id == product.id
                 )
            )
    )
    result = await session.execute(query)
    val = result.scalar()
    print(val)
    if val:
        raise HTTPException(
            status_code=401,
            detail="Данный продукт Уже добавлен в ваш вишлист."
        )
    return product


async def update_interest_row(
    product: int = Depends(validate_favorite),
    session: AsyncSession = Depends(get_async_session)
):
    up = (
        update(Product).
        where(Product.id == product.id).
        values(interest=Product.interest+1)
    )
    await session.execute(up)
    await session.commit()
    return product
