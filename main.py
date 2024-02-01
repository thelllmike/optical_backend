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

# Endpoint to get all lenses
# @app.get("/lenses")
# async def get_lenses():
#     with engine.connect() as connection:
#         result = connection.execute(select(lenses))
#         lenses_list = [dict(row._mapping) for row in result]  # Updated conversion
#         return lenses_list

# @app.get("/frames")
# async def get_frames():
#     with engine.connect() as connection:
#         result = connection.execute(select(frames))
#         frames_list = [dict(row._mapping) for row in result]  # Updated conversion
#         return frames_list



# # Endpoint to add a lens
# @app.post("/add_lens")
# async def add_lens(lens_data: LensCreate):
#     query = lenses.insert().values(**lens_data.dict())
#     with engine.begin() as connection:  # Use begin() to start a transaction
#         try:
#             result = connection.execute(query)
#             return {"id": result.inserted_primary_key[0]}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to add a frame
# @app.post("/add_frame")
# async def add_frame(frame_data: FrameCreate):
#     query = frames.insert().values(**frame_data.dict())
#     with engine.begin() as connection:  # Use begin() to start a transaction
#         try:
#             result = connection.execute(query)
#             return {"id": result.inserted_primary_key[0]}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to update a lens
# @app.put("/add_lens/{id}")
# async def add_lens(id: int, lens_data: LensUpdate):
#     query = update(lenses).where(lenses.c.id == id).values(**lens_data.dict(exclude_unset=True))
#     with engine.begin() as connection:
#         result = connection.execute(query)
#         if result.rowcount == 0:
#             raise HTTPException(status_code=404, detail="Lens not found")
#         return {"message": "Lens updated successfully"}

# # Endpoint to delete a lens
# @app.delete("/add_lens/{id}")
# async def add_lens(id: int):
#     query = delete(lenses).where(lenses.c.id == id)
#     with engine.begin() as connection:
#         result = connection.execute(query)
#         if result.rowcount == 0:
#             raise HTTPException(status_code=404, detail="Lens not found")
#         return {"message": "Lens deleted successfully"}
    
# # Endpoint to update a frame
# @app.put("/add_frame/{id}")
# async def update_frame(id: int, frame_data: FrameUpdate):
#     query = update(frames).where(frames.c.id == id).values(**frame_data.dict(exclude_unset=True))
#     with engine.begin() as connection:
#         result = connection.execute(query)
#         if result.rowcount == 0:
#             raise HTTPException(status_code=404, detail="Frame not found")
#         return {"message": "Frame updated successfully"}

# # Endpoint to delete a frame
# @app.delete("/add_frame/{id}")
# async def delete_frame(id: int):
#     query = delete(frames).where(frames.c.id == id)
#     with engine.begin() as connection:
#         result = connection.execute(query)
#         if result.rowcount == 0:
#             raise HTTPException(status_code=404, detail="Frame not found")
#         return {"message": "Frame deleted successfully"}