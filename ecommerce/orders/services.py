from typing import List

from fastapi import HTTPException, status

from ecommerce.cart.models import Cart, CartItems
from ecommerce.orders.models import Order, OrderDetails
from ecommerce.user.models import User


async def initiate_order(database) -> Order:
    user_info = database.query(User).filter(User.email == "zombie@mailinator.com").first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")

    cart = database.query(Cart).filter(Cart.user_id == user_info.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cart for this user!")

    cart_items = database.query(CartItems).filter(Cart.id == cart.id)
    if not cart_items.count():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found in cart!")

    total_amount: float = 0.0
    for item in cart_items:
        total_amount += item.products.price

    new_order = Order(order_amount=total_amount, customer_id=user_info.id, shipping_address="587 Hinkle Deegan Lake Road, Syracus, New York")
    database.add(new_order)
    database.commit()
    database.refresh(new_order)

    bulk_order_details = list()

    for item in cart_items:
        new_order_details = OrderDetails(order_id=new_order.id, product_id=item.products.id)
        bulk_order_details.append(new_order_details)

    database.bulk_save_objects(bulk_order_details)
    database.commit()

    # TODO: Send Email to alert user on placed order

    # Clear items in the cart
    database.query(CartItems).filter(CartItems.cart_id == cart.id).delete()
    database.commit()

    return new_order



async def order_list(database) -> List[Order]:
    user_info = database.query(User).filter(User.email == "zombie@mailinator.com").first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")

    orders = database.query(Order).filter(Order.customer_id == user_info.id).all()
    return orders



