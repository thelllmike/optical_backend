from winreg import HKEY_CURRENT_USER
from fastapi import Body, FastAPI, HTTPException, Depends, Query, status, APIRouter , Header
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List
from jose import jwt 
from sqlalchemy.orm import sessionmaker
from models.model import lenses, frames  
from schemas.schemas import LensCreate, FrameCreate, LensUpdate, FrameUpdate
from database import SessionLocal
from database import engine
from sqlalchemy.exc import SQLAlchemyError




router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()





@router.get("/lenses")
async def get_lenses(branch_id: int = Query(..., description="The ID of the branch to filter lenses by")):
    with engine.connect() as connection:
        result = connection.execute(select(lenses).where(lenses.c.branch_id == branch_id))
        lenses_list = [dict(row._mapping) for row in result]
        return lenses_list

@router.get("/frames")
async def get_frames(branch_id: int = Query(..., description="The ID of the branch to filter frames by")):
    with engine.connect() as connection:
        result = connection.execute(select(frames).where(frames.c.branch_id == branch_id))
        frames_list = [dict(row._mapping) for row in result]
        return frames_list


# Endpoint to add a lens
@router.post("/add_lens")
async def add_lens(lens_data: LensCreate):
    query = lenses.insert().values(**lens_data.dict())
    with engine.begin() as connection:  # Use begin() to start a transaction
        try:
            result = connection.execute(query)
            return {"id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a frame
@router.post("/add_frame")
async def add_frame(frame_data: FrameCreate):
    query = frames.insert().values(**frame_data.dict())
    with engine.begin() as connection:  # Use begin() to start a transaction
        try:
            result = connection.execute(query)
            return {"id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update a lens
@router.put("/add_lens/{id}")
async def add_lens(id: int, lens_data: LensUpdate):
    query = update(lenses).where(lenses.c.id == id).values(**lens_data.dict(exclude_unset=True))
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Lens not found")
        return {"message": "Lens updated successfully"}

# Endpoint to delete a lens
@router.delete("/add_lens/{id}")
async def add_lens(id: int):
    query = delete(lenses).where(lenses.c.id == id)
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Lens not found")
        return {"message": "Lens deleted successfully"}
    
# Endpoint to update a frame
@router.put("/add_frame/{id}")
async def update_frame(id: int, frame_data: FrameUpdate):
    query = update(frames).where(frames.c.id == id).values(**frame_data.dict(exclude_unset=True))
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Frame not found")
        return {"message": "Frame updated successfully"}

# Endpoint to delete a frame
@router.delete("/add_frame/{id}")
async def delete_frame(id: int):
    query = delete(frames).where(frames.c.id == id)
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Frame not found")
        return {"message": "Frame deleted successfully"}
    
# #update lens stock
# @router.put("/update-lens-stock/{branch_id}/{lens_id}")
# async def update_lens_stock(branch_id: int, lens_id: int, quantity: int):
#     with engine.begin() as connection:  # Use begin() to start a transaction
#         # Fetch the current stock for the lens
#         select_stmt = select(lenses.c.stock).where(lenses.c.id == lens_id, lenses.c.branch_id == branch_id)
#         current_stock_result = connection.execute(select_stmt).scalar()

#         if current_stock_result is None:
#             raise HTTPException(status_code=404, detail="Lens not found")
        
#         current_stock = current_stock_result
#         if current_stock < quantity:
#             raise HTTPException(status_code=400, detail="Not enough stock available")

#         # Deduct the quantity from the stock
#         new_stock = current_stock - quantity
#         update_stmt = update(lenses).where(lenses.c.id == lens_id, lenses.c.branch_id == branch_id).values(stock=new_stock)
        
#         try:
#             result = connection.execute(update_stmt)
#             if result.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="Lens not found")
#             return {"message": "Stock updated successfully", "new_stock": new_stock}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))
        
# #update frame stock
# @router.put("/update-frame-stock/{branch_id}/{frame_id}")
# async def update_frame_stock(branch_id: int, frame_id: int, quantity: int):
#     with engine.begin() as connection:  # Use begin() to start a transaction
#         # Fetch the current stock for the frame
#         select_stmt = select(frames.c.stock).where(frames.c.id == frame_id, frames.c.branch_id == branch_id)
#         current_stock_result = connection.execute(select_stmt).scalar()

#         if current_stock_result is None:
#             raise HTTPException(status_code=404, detail="Frame not found")
        
#         current_stock = current_stock_result
#         if current_stock < quantity:
#             raise HTTPException(status_code=400, detail="Not enough stock available")

#         # Deduct the quantity from the stock
#         new_stock = current_stock - quantity
#         update_stmt = update(frames).where(frames.c.id == frame_id, frames.c.branch_id == branch_id).values(stock=new_stock)
        
#         try:
#             result = connection.execute(update_stmt)
#             if result.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="Frame not found")
#             return {"message": "Stock updated successfully", "new_stock": new_stock}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update-lens-stock")
async def update_lens_stock(update_data: dict = Body(...)):
    branch_id = update_data.get("branch_id")
    lens_id = update_data.get("lens_id")
    quantity = update_data.get("quantity")
    
    with engine.begin() as connection:
        select_stmt = select(lenses.c.stock).where(lenses.c.id == lens_id, lenses.c.branch_id == branch_id)
        current_stock_result = connection.execute(select_stmt).scalar()

        if current_stock_result is None:
            raise HTTPException(status_code=404, detail="Lens not found")

        current_stock = current_stock_result
        if current_stock < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        new_stock = current_stock - quantity
        update_stmt = update(lenses).where(lenses.c.id == lens_id, lenses.c.branch_id == branch_id).values(stock=new_stock)

        try:
            result = connection.execute(update_stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Lens not found")
            return {"message": "Stock updated successfully", "new_stock": new_stock}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/update-frame-stock")
async def update_frame_stock(update_data: dict = Body(...)):
    branch_id = update_data.get("branch_id")
    frame_id = update_data.get("frame_id")
    quantity = update_data.get("quantity")
    
    with engine.begin() as connection:
        select_stmt = select(frames.c.stock).where(frames.c.id == frame_id, frames.c.branch_id == branch_id)
        current_stock_result = connection.execute(select_stmt).scalar()

        if current_stock_result is None:
            raise HTTPException(status_code=404, detail="Frame not found")

        current_stock = current_stock_result
        if current_stock < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        new_stock = current_stock - quantity
        update_stmt = update(frames).where(frames.c.id == frame_id, frames.c.branch_id == branch_id).values(stock=new_stock)

        try:
            result = connection.execute(update_stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Frame not found")
            return {"message": "Stock updated successfully", "new_stock": new_stock}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))