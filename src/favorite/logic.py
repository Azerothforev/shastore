from sqlalchemy import and_, delete, select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from auth.models import User
from auth.config import current_user
from database import get_async_session
from favorite.dependencies import downgrade_interest
from product.models import Favorite, Product


async def get_to_favorites_product(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        join(Favorite).
        where(Favorite.user_id == user.id).
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


async def downgrade_favorites_product(
    product_id: int = Depends(downgrade_interest),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        delete(Favorite).
        where(
            and_(Favorite.user_id == user.id,
                 Favorite.product_id == product_id
                 )
            )
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Товар удален из вашего вишлист."}
