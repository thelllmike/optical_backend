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

@router.get("/onlyframe")
async def get_frames():
    with Session(engine) as session:
        # SQL query to select only the 'frame' column
        sql = text("SELECT frame FROM frames")
        result = session.execute(sql)
        # Extract frame names and create a list
        frame_names = [row[0] for row in result]  # Access the first column of each tuple
        return frame_names

