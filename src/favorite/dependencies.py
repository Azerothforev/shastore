from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.models import Product


async def downgrade_interest(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    down = (
        update(Product).
        where(Product.id == product_id).
        values(interest=Product.interest-1)
    )
    await session.execute(down)
    await session.commit()
    return product_id
