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

@router.get("/onlycategory")
async def get_lens_categories(branch_id: int, db: Session = Depends(get_db)):
    # SQL query to select distinct values from the 'category' column filtered by branch_id
    sql = text("SELECT DISTINCT category FROM lenses WHERE branch_id = :branch_id")
    result = db.execute(sql, {'branch_id': branch_id})
    # Extract unique category names and create a list
    category_names = [row[0] for row in result]
    return category_names


@router.get("/coatings-by-category")
async def get_coatings_by_category(category: str = Query(...), branch_id: int = Query(...), db: Session = Depends(get_db)):
    # SQL query to select distinct coating values where the category and branch_id match
    sql = text("SELECT DISTINCT coating FROM lenses WHERE category = :category AND branch_id = :branch_id")
    result = db.execute(sql, {'category': category, 'branch_id': branch_id})
    # Extract unique coatings for the specified category and branch_id
    coatings = [row[0] for row in result]
    return coatings

@router.get("/powers-by-category-and-coating")
async def get_powers_by_category_and_coating(category: str = Query(...), coating: str = Query(...), branch_id: int = Query(...), db: Session = Depends(get_db)):
    # SQL query to select distinct power values where category, coating, and branch_id match
    sql = text("""
        SELECT DISTINCT power 
        FROM lenses 
        WHERE category = :category 
        AND coating = :coating 
        AND branch_id = :branch_id
    """)
    result = db.execute(sql, {'category': category, 'coating': coating, 'branch_id': branch_id})
    # Extract unique powers for the specified category, coating, and branch_id
    powers = [row[0] for row in result]
    return powers

@router.get("/lens-price-by-selection")
async def get_lens_price_by_selection(
    category: str = Query(...), 
    coating: str = Query(...), 
    power: float = Query(...),
    branch_id: int = Query(...),  # Add branch_id as a query parameter
    db: Session = Depends(get_db)
):
    # SQL query to select the price for the specified lens selection and branch_id
    sql = text("""
        SELECT selling_price 
        FROM lenses 
        WHERE category = :category 
        AND coating = :coating 
        AND power = :power
        AND branch_id = :branch_id  # Include branch_id in the WHERE clause
    """)
    result = db.execute(sql, {
        'category': category, 
        'coating': coating, 
        'power': power,
        'branch_id': branch_id  # Pass branch_id to the query
    }).first()

    if result:
        return {"price": result[0]}
    else:
        return {"price": "Not available"}

