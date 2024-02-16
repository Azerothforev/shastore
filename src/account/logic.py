from fastapi import Depends
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from account.dependencies import valid_product
from account.models import Order
from account.schemas import UpdateProduct
from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.models import Product


async def get_current_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(User).
        where(User.id == user.id)
    )
    res = await session.execute(query)
    return res.scalar()


async def get_user_product(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(and_(
            Product.seller_id == user.id,
            Product.status == 0)
        ).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    res = await session.execute(query)
    return res.scalars().all()


async def get_order_product(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        join(Order).
        where(Order.buyer_id == user.id).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    res = await session.execute(query)
    return res.scalars().all()


async def get_sales_product(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        join(Order).
        where(Order.seller_id == user.id).
        options(
            joinedload(Product.seller),
            joinedload(Product.brand),
            joinedload(Product.color),
            joinedload(Product.state),
            joinedload(Product.category),
        )
    )
    res = await session.execute(query)
    return res.scalars().all()


async def delete_product(
    product_id: int = Depends(valid_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    print(product_id)
    stmt = (
        delete(Product).
        where(Product.id == product_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Вы успешно сняли с публикации свой товар"}


async def update_user_product(
    update_product: UpdateProduct,
    product_id: int = Depends(valid_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(Product.id == product_id)
    )
    res = await session.execute(query)
    up_product = res.scalar()
    for field, value in update_product.dict(exclude_unset=True).items():
        if value != 0 and value != "string":
            setattr(up_product, field, value)

    await session.commit()
    await session.refresh(up_product)
    return {"status": "Ваш продукт успешно обновлен."}
