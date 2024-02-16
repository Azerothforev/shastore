import asyncio
from fastapi import FastAPI

from auth.config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from product.router import router as product_router
from favorite.router import router as favorite_router
from cart.router import router as cart_router
from account.router import router as account_router
from rabbitmqconnect.connection import RabbitMQConnection
from rabbitmqconnect.read_queue import listen_to_queue
app = FastAPI(
    title="shastore"
)


@app.on_event("startup")
async def startup():
    await RabbitMQConnection.get_connection()


@app.on_event("shutdown")
async def shutdown():
    conn = RabbitMQConnection._connection
    if conn and not conn.is_closed:
        await conn.close()


@app.on_event("startup")
async def startup_read():
    asyncio.create_task(listen_to_queue())

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(product_router)
app.include_router(favorite_router)
app.include_router(cart_router)
app.include_router(account_router)
