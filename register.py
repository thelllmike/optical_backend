from collections import UserString
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mysqlx import Session
from sqlalchemy import Engine, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, engine_from_config
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import SessionLocal
from database import engine
from models.register import metadata, optical_shops , branches , users
from schemas.register import BranchCreate, OpticalShopCreate, OpticalShopUpdate, UserCreate

from passlib.context import CryptContext


from fastapi import APIRouter

router = APIRouter()
# Define your tables (assuming they are already defined in your database)

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

@router.post("/create/optical_shop")
async def create_optical_shop(shop: OpticalShopCreate, db: Session = Depends(get_db)):
    try:
        query = optical_shops.insert().values(**shop.dict())
        result = db.execute(query)
        db.commit()
        return {"id": result.inserted_primary_key[0]}
    except IntegrityError as e:
        db.rollback()
        # Check if it's a duplicate email error
        if "Duplicate entry" in str(e) and "for key 'optical_shops.email'" in str(e):
            raise HTTPException(status_code=400, detail="This email is already in use.")
        else:
            raise HTTPException(status_code=500, detail=str(e))




# Endpoint to create a branch
@router.post("/create/branch")
async def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    # Convert Pydantic model to dict and insert into the database using SQLAlchemy
    query = branches.insert().values(**branch.dict())
    result = db.execute(query)
    db.commit()  # Commit the transaction
    return {"id": result.inserted_primary_key[0]}

# Endpoint to create a user
@router.post("/create/user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Convert Pydantic model to dict and insert into the database using SQLAlchemy
    # Assuming 'user' is your Pydantic model
    hashed_password = hash_password(user.password)  # Replace with your actual password hashing method
    user_data = user.dict()
    user_data['password'] = hashed_password
    query = users.insert().values(**user_data)
    result = db.execute(query)
    db.commit()  # Commit the transaction
    return {"id": result.inserted_primary_key[0]}