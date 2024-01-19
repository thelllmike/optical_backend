from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from database import engine
from models.model import metadata, lenses, frames

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

#frames
@router.get("/onlyframe")
async def get_frames():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT frame FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_names = [row[0] for row in result]  # Access the first column of each tuple
        return frame_names
    
@router.get("/onlybrand")
async def get_brand():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT brand FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_brand = [row[0] for row in result]  # Access the first column of each tuple
        return frame_brand

@router.get("/onlysize")
async def get_size():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT size FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_size = [row[0] for row in result]  # Access the first column of each tuple
        return frame_size
    
@router.get("/onlycolor")
async def get_color():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT color FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_color = [row[0] for row in result]  # Access the first column of each tuple
        return frame_color
    
@router.get("/onlymodel")
async def get_model():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT model FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_model = [row[0] for row in result]  # Access the first column of each tuple
        return frame_model

