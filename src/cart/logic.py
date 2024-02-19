import aio_pika
from sqlalchemy import and_, delete, insert, select
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from account.models import Order
from auth.models import User
from auth.config import current_user
from cart.dependencies import upgrade_status_product
from database import get_async_session
from product.models import Cart, Product
from rabbitmqconnect.connection import RabbitMQConnection


async def get_to_carts_product(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        join(Cart).
        where(Cart.user_id == user.id).
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
    if not product:
        raise HTTPException(
            status_code=404,
            detail='У вас нет товара в корзине.'
        )
    return product


async def downgrade_carts_product(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        delete(Cart).
        where(
            and_(Cart.user_id == user.id,
                 Cart.product_id == product_id
                 )
            )
    )
    await session.execute(stmt)
    await session.commit()


async def buy_product(
    product: int = Depends(upgrade_status_product),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    rabbitmq_session: RabbitMQConnection = Depends(
        RabbitMQConnection.get_connection),
):
    stmt = (
        insert(Order).
        values(
            product_id=product.id,
            seller_id=product.seller_id,
            buyer_id=user.id)
    )
    await rabbitmq_session[3].publish(
        aio_pika.Message(body=(user.email + ' buy').encode()),
        routing_key="add product/success register"
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "вы приобрели товар, ожидайте получения"}
