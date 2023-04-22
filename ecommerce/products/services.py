from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models
from . import schema


async def create_new_category(request, database) -> models.Category:
    new_category = models.Category(name=request.name)
    database.add(new_category)
    database.commit()
    database.refresh(new_category)
    return new_category


async def get_all_categories(database) -> List[schema.DisplayCategory]:
    categories = database.query(models.Category).all()

    return categories


async def get_category_by_id(id, database) -> models.Category:
    category_info = database.query(models.Category).get(id)
    if not category_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    return category_info


async def delete_category(id, database):
    database.query(models.Category).filter(models.Category.id == id).delete()
    database.commit()


async def create_new_product(request, database) -> models.Product:
    new_product = models.Product(name=request.name, quantity=request.quantity, description=request.description,
                                 price=request.price, category_id=request.category_id)

    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


async def get_all_products(db_session: Session) -> List[models.Product]:
    products = db_session.query(models.Product).all()

    return products


async def get_product_by_id(id: int, db_session: Session) -> models.Product:
    product_info = db_session.query(models.Product).get(id)
    if not product_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    return product_info
