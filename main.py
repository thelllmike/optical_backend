# main.py
from fastapi import FastAPI, HTTPException, applications
from mysqlx import Session
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
# from models.model import metadata, lenses, frames
from schemas.schemas import LensCreate, FrameCreate, LensUpdate, FrameUpdate
from fastapi.middleware.cors import CORSMiddleware
from billing import router as billing_router
from dropdown import router as dropdown_router
from register import router as register_router
from product import router as product_router

from sqlalchemy.orm import sessionmaker




# Include the billing router with the app instance

def get_db():
     db = Session(bind=engine)
     try:
         yield db
     finally:
         db.close()



from database import engine
from models.model import metadata

metadata.create_all(bind=engine)
# Database URL
# DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# metadata.create_all(engine)

# Create a FastAPI instance
app = FastAPI()
app.include_router(billing_router, prefix="/billing", tags=["billing"])
app.include_router(dropdown_router, prefix="/dropdown", tags=["dropdown"])
app.include_router(register_router, prefix="/register", tags=["register"])
app.include_router(product_router, prefix="/product", tags=["product"])
# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

