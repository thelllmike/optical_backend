from models.model import lenses, frames
from databases import Database

async def create_lens(db: Database, lens_data: dict):
    query = lenses.insert().values(**lens_data)
    return await db.execute(query)

async def create_frame(db: Database, frame_data: dict):
    query = frames.insert().values(**frame_data)
    return await db.execute(query)

# Add more CRUD functions as needed
