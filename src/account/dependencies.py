from fastapi import Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.models import Product


async def valid_product(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(
            and_(Product.id == product_id,
                 Product.seller_id == user.id)
        )
    )
    res = await session.execute(query)
    if not res.scalar():
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    return product_id
