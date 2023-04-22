from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from ecommerce import db
from ecommerce.user.schema import User
from . import schema
from . import services

router = APIRouter(tags=["Cart"], prefix='/cart')


@router.post("/product/{id}", status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(id: int, database: Session = Depends(db.get_db)):
    result = await services.add_product_to_cart(id, database)
    return result


@router.get("/products", response_model=schema.ShowCart)
async def get_all_products_in_cart(database: Session = Depends(db.get_db)):
    result = await services.get_all_items(database)
    return result


@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_product_from_cart(id: int, database: Session = Depends(db.get_db)):
    result = await services.remove_cart_item(id, database)
    # return result
