from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from database import engine
from models.model import metadata, lenses, frames
from fastapi import Query

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
@router.get("/onlyframe")
async def get_frames():
    with Session(engine) as session:
        # SQL query to select distinct values from the 'frame' column
        sql = text("SELECT DISTINCT frame FROM frames")
        result = session.execute(sql)
        # Extract unique frame names and create a list
        frame_names = [row[0] for row in result]
        return frame_names
    
@router.get("/onlybrand")
async def get_brand():
    with Session(engine) as session:
        # SQL query to select distinct values from the 'brand' column
        sql = text("SELECT DISTINCT brand FROM frames")
        result = session.execute(sql)
        # Extract unique brand names and create a list
        frame_brand = [row[0] for row in result]
        return frame_brand

#filter by frames which we selected 
@router.get("/brands-by-frame")
async def get_brands_by_frame(frame: str = Query(...)):  # '...' makes the query parameter required
    with Session(engine) as session:
        # SQL query to select distinct brand values where the frame matches
        sql = text("SELECT DISTINCT brand FROM frames WHERE frame = :frame")
        result = session.execute(sql, {'frame': frame})
        # Extract unique brands for the specified frame
        brands = [row[0] for row in result]
        return brands

@router.get("/onlysize")
async def get_size():
    with Session(engine) as session:
        # SQL query to select distinct values from the 'size' column
        sql = text("SELECT DISTINCT size FROM frames")
        result = session.execute(sql)
        # Extract unique sizes and create a list
        frame_size = [row[0] for row in result]
        return frame_size
    
@router.get("/onlycolor")
async def get_color():
    with Session(engine) as session:
        # SQL query to select distinct values from the 'color' column
        sql = text("SELECT DISTINCT color FROM frames")
        result = session.execute(sql)
        # Extract unique colors and create a list
        frame_color = [row[0] for row in result]
        return frame_color
    
@router.get("/onlymodel")
async def get_model():
    with Session(engine) as session:
        # SQL query to select distinct values from the 'model' column
        sql = text("SELECT DISTINCT model FROM frames")
        result = session.execute(sql)
        # Extract unique models and create a list
        frame_model = [row[0] for row in result]
        return frame_model
