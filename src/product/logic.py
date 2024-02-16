from typing import Mapping
from fastapi import Depends
from sqlalchemy import insert, or_, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.dependencies import update_interest_row, validate_cart
from product.models import Brand, Cart, Favorite, Product
from product.schemas import ProductCreate


async def fin_to_brand(
    brand_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(Product.brand_id == brand_id).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    res = await session.execute(query)
    product = res.scalars().all()
    return product


async def get_products_by_search(
    search: str,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product)
        .join(Brand, Product.brand_id == Brand.id)
        .join(User, Product.seller_id == User.id)
        .where(
            or_(
                Brand.name.ilike(f'%{search}%'),
                User.username.ilike(f'%{search}%')
            )
        )
        .options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )

    result = await session.execute(query)
    return result.scalars().all()


async def get_all_product(
    session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(Product).
        where(Product.status == 0).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_one_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(
            and_(
                Product.id == product_id,
                Product.status == 0
            )
        ).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    result = await session.execute(query)
    return result.scalars().all()


async def create_product(
    new_product: ProductCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_product_dict = new_product.dict()
    new_product_dict['seller_id'] = user.id
    stmt = (
        insert(Product).
        values(**new_product_dict)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Продукт успешно опубликован."}


async def add_to_cart(
    new_product: Mapping = Depends(validate_cart),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        insert(Cart).
        values(
            user_id=user.id,
            product_id=new_product.id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Продукт успешно добавлен в корзину."}


async def add_to_favorite(
    new_product: Mapping = Depends(update_interest_row),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        insert(Favorite).
        values(
            user_id=user.id,
            product_id=new_product.id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Продукт успешно добавлен в вишлист."}
