# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from models.model import metadata, lenses, frames
from schemas.schemas import LensCreate, FrameCreate, LensUpdate, FrameUpdate



# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# Create a FastAPI instance
app = FastAPI()

# Endpoint to get all lenses
@app.get("/lenses/")
async def get_lenses():
    with engine.connect() as connection:
        result = connection.execute(select(lenses))
        lenses_list = [dict(row._mapping) for row in result]  # Updated conversion
        return lenses_list

@app.get("/frames/")
async def get_frames():
    with engine.connect() as connection:
        result = connection.execute(select(frames))
        frames_list = [dict(row._mapping) for row in result]  # Updated conversion
        return frames_list



# Endpoint to add a lens
@app.post("/add_lens/")
async def add_lens(lens_data: LensCreate):
    query = lenses.insert().values(**lens_data.dict())
    with engine.begin() as connection:  # Use begin() to start a transaction
        try:
            result = connection.execute(query)
            return {"id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a frame
@app.post("/add_frame/")
async def add_frame(frame_data: FrameCreate):
    query = frames.insert().values(**frame_data.dict())
    with engine.begin() as connection:  # Use begin() to start a transaction
        try:
            result = connection.execute(query)
            return {"id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update a lens
@app.put("/update_lens/{lens_id}")
async def update_lens(lens_id: int, lens_data: LensUpdate):
    query = update(lenses).where(lenses.c.id == lens_id).values(**lens_data.dict(exclude_unset=True))
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Lens not found")
        return {"message": "Lens updated successfully"}

# Endpoint to delete a lens
@app.delete("/delete_lens/{lens_id}")
async def delete_lens(lens_id: int):
    query = delete(lenses).where(lenses.c.id == lens_id)
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Lens not found")
        return {"message": "Lens deleted successfully"}
    
# Endpoint to update a frame
@app.put("/update_frame/{frame_id}")
async def update_frame(frame_id: int, frame_data: FrameUpdate):
    query = update(frames).where(frames.c.id == frame_id).values(**frame_data.dict(exclude_unset=True))
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Frame not found")
        return {"message": "Frame updated successfully"}

# Endpoint to delete a frame
@app.delete("/delete_frame/{frame_id}")
async def delete_frame(frame_id: int):
    query = delete(frames).where(frames.c.id == frame_id)
    with engine.begin() as connection:
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Frame not found")
        return {"message": "Frame deleted successfully"}