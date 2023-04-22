from typing import Union

from fastapi import FastAPI
from ecommerce.user import router as user_router
from ecommerce.products import router as product_router
from ecommerce.cart import router as cart_router
from ecommerce.orders import router as orders_router

app = FastAPI(title="WeSabiAll API", description="API for exposing endpoints our ecommerce store", version="1.0.0")

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(orders_router.router)
