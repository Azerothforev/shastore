from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


from auth.models import User
from auth.config import current_user
from database import get_async_session
from product.dependencies import validate_product
from product.models import Product


async def upgrade_status_product(
    product: int = Depends(validate_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    up_status = (
        update(Product).
        where(Product.id == product.id).
        values(status=1)
    )
    await session.execute(up_status)
    await session.commit()
    return product
