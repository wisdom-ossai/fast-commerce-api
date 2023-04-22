from typing import List

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ecommerce import db

from ecommerce.products.models import Product
from .models import Cart, CartItems
from .schema import ShowCart
from ecommerce.user.models import User


async def add_items(cart_id, product_id, database: Session = Depends(db.get_db)):
    cat_item = database.query(CartItems).filter(CartItems.product_id == product_id).first()
    if cat_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already added to cart")
    cart_items = CartItems(cart_id=cart_id, product_id=product_id)
    database.add(cart_items)
    database.commit()
    database.refresh(cart_items)


async def add_product_to_cart(id: int, db_session: Session):
    product = db_session.query(Product).get(id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product out of stock")

    user_info = db_session.query(User).filter(User.email == 'zombie@mailinator.com').first()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")

    cart_info = db_session.query(Cart).filter(Cart.user_id == user_info.id).first()

    if not cart_info:
        new_cart = Cart(user_id=user_info.id)
        db_session.add(new_cart)
        db_session.commit()
        db_session.refresh(new_cart)
        await add_items(new_cart.id, product.id, db_session)
    else:
        await add_items(cart_info.id, product.id, db_session)
    return {"status": status.HTTP_201_CREATED, "message": "Item added to cart"}


async def get_all_items(database: Session) -> ShowCart:
    user_info = database.query(User).filter(User.email == 'zombie@mailinator.com').first()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")

    cart = database.query(Cart).filter(Cart.user_id == user_info.id).first()
    return cart


async def remove_cart_item(id: int, database: Session):
    user_info = database.query(User).filter(User.email == 'zombie@mailinator.com').first()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")

    cart = database.query(Cart).filter(Cart.user_id == user_info.id).first()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no cart!")
    database.query(CartItems).filter(CartItems.id == id, CartItems.cart_id == cart.id).delete()

    database.commit()
    return
    # return {"message": 'Product removed from cart'}
