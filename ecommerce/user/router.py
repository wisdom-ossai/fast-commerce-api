from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ecommerce import db
from typing import List
from . import schema
from . import services
from . import validator
from .models import User

router = APIRouter(tags=['Users'], prefix='/user')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.User, database: Session = Depends(db.get_db)):
    user = await validator.verify_email_exist(request.email, database)

    if user:
        raise HTTPException(status_code=400, detail='The user with this email already exists in the system.')

    new_user: User = await services.new_user_register(request, database)
    return new_user


@router.get("/", response_model=List[schema.DisplayUser])
async def get_all_users(database: Session = Depends(db.get_db)):
    return await services.all_users(database)


@router.get('/{id}', response_model=schema.DisplayUser)
async def get_user_by_id(id: int, database: Session = Depends(db.get_db)):
    return await services.get_user(id, database)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(id: int, database: Session = Depends(db.get_db)):
    return await services.delete_user(id, database)
