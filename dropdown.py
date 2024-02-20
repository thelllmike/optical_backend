from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from database import SessionLocal, engine
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
async def get_frames(branch_id: int, db: Session = Depends(get_db)):
    # SQL query to select distinct values from the 'frame' column filtered by branch_id
    sql = text("SELECT DISTINCT frame FROM frames WHERE branch_id = :branch_id")
    result = db.execute(sql, {'branch_id': branch_id})
    # Extract unique frame names and create a list
    frame_names = [row[0] for row in result]
    return frame_names



@router.get("/brands-by-frame")
async def get_brands_by_frame(frame: str = Query(...), branch_id: int = Query(...), db: Session = Depends(get_db)):
    # SQL query to select distinct brand values where the frame and branch_id match
    sql = text("SELECT DISTINCT brand FROM frames WHERE frame = :frame AND branch_id = :branch_id")
    result = db.execute(sql, {'frame': frame, 'branch_id': branch_id})
    # Extract unique brands for the specified frame and branch_id
    brands = [row[0] for row in result]
    return brands
    


@router.get("/sizes-by-frame-and-brand")
async def get_sizes_by_frame_and_brand(frame: str = Query(...), brand: str = Query(...), branch_id: int = Query(...), db: Session = Depends(get_db)):
    # SQL query to select distinct size values where frame, brand, and branch_id match
    sql = text("""
        SELECT DISTINCT size 
        FROM frames 
        WHERE frame = :frame 
        AND brand = :brand 
        AND branch_id = :branch_id
    """)
    result = db.execute(sql, {'frame': frame, 'brand': brand, 'branch_id': branch_id})
    # Extract unique sizes for the specified frame, brand, and branch_id
    sizes = [row[0] for row in result]
    return sizes
    


@router.get("/colors-by-frame-brand-size")
async def get_colors_by_frame_brand_size(
    frame: str = Query(...), 
    brand: str = Query(...), 
    size: str = Query(...), 
    branch_id: int = Query(...),  # Add branch_id as a query parameter
    db: Session = Depends(get_db)
):
    # SQL query to select distinct color values where frame, brand, size, and branch_id match
    sql = text("""
        SELECT DISTINCT color 
        FROM frames 
        WHERE frame = :frame 
        AND brand = :brand 
        AND size = :size
        AND branch_id = :branch_id  # Include branch_id in the WHERE clause
    """)
    result = db.execute(sql, {'frame': frame, 'brand': brand, 'size': size, 'branch_id': branch_id})
    # Extract unique colors for the specified frame, brand, size, and branch_id
    colors = [row[0] for row in result]
    return colors



@router.get("/models-by-selection")
async def get_models_by_selection(
    frame: str = Query(...), 
    brand: str = Query(...), 
    size: str = Query(...), 
    color: str = Query(...),
    branch_id: int = Query(...),
    db: Session = Depends(get_db)
):
    sql = text("""
        SELECT DISTINCT model 
        FROM frames 
        WHERE frame = :frame 
        AND brand = :brand 
        AND size = :size
        AND color = :color
        AND branch_id = :branch_id
    """)
    result = db.execute(sql, {
        'frame': frame, 
        'brand': brand, 
        'size': size, 
        'color': color,
        'branch_id': branch_id
    }).fetchall()
    
    models = [row[0] for row in result]  # Corrected this line
    return models




# @router.get("/price-by-selection")
# async def get_price_by_selection(
#     frame: str = Query(...), 
#     brand: str = Query(...), 
#     size: str = Query(...), 
#     color: str = Query(...),
#     model: str = Query(...),
#     branch_id: int = Query(...),  # Add branch_id as a query parameter
#     db: Session = Depends(get_db)
# ):
#     # SQL query to select the price for the specified selection and branch_id
#     sql = text("""
#         SELECT selling_price 
#         FROM frames 
#         WHERE frame = :frame 
#         AND brand = :brand 
#         AND size = :size
#         AND color = :color
#         AND model = :model
#         AND branch_id = :branch_id  # Include branch_id in the WHERE clause
#     """)
#     result = db.execute(sql, {
#         'frame': frame, 
#         'brand': brand, 
#         'size': size, 
#         'color': color, 
#         'model': model,
#         'branch_id': branch_id  # Pass branch_id to the query
#     }).first()

#     if result:
#         return {"price": result[0]}
#     else:
#         return {"price": "Not available"}

@router.get("/price-by-selection")
async def get_price_by_selection(
    frame: str = Query(...), 
    brand: str = Query(...), 
    size: str = Query(...), 
    color: str = Query(...),
    model: str = Query(...),
    branch_id: int = Query(...),  # Added branch_id as a query parameter
    db: Session = Depends(get_db)
):
    # SQL query to select the id and price for the specified frame selection and branch_id
    sql = text("""
        SELECT id, selling_price 
        FROM frames 
        WHERE frame = :frame 
        AND brand = :brand 
        AND size = :size
        AND color = :color
        AND model = :model
        AND branch_id = :branch_id  # Include branch_id in the WHERE clause
    """)
    result = db.execute(sql, {
        'frame': frame, 
        'brand': brand, 
        'size': size, 
        'color': color, 
        'model': model,
        'branch_id': branch_id  # Pass branch_id to the query
    }).first()

    if result:
        return {"id": result[0], "price": result[1]}  # Return both id and price
    else:
        return {"message": "Frame not available"}