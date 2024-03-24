from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import distinct, extract, func
from sqlalchemy.orm import Session
from database import SessionLocal
from models.billing import customers, billings, billing_items, payment_details
from models.model import frames , lenses
from datetime import datetime, timezone
import pytz
router = APIRouter()

colombo_zone = pytz.timezone('Asia/Colombo')
colombo_now = datetime.now(colombo_zone)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/billing-details")
async def get_billing_details(branch_id: int = Query(...), db: Session = Depends(get_db)):
    # Execute the SQL query
    query_result = db.query(
        billings.c.invoice_date.label("invoice_date"),
        customers.c.full_name.label("customer_name"),
        customers.c.mobile_number.label("mobile_number"),
        billings.c.sales_person.label("sales_person"),
        lenses.c.category.label("lens_category"),
        frames.c.frame.label("frame_brand"),
        payment_details.c.advance_paid.label("advance_paid"),
        payment_details.c.grand_total.label("grand_total"),
        payment_details.c.balance_amount.label("balance_amount"),
        payment_details.c.pay_type.label("pay_type")
    ).join(customers, billings.c.customer_id == customers.c.id)\
    .join(billing_items, billings.c.id == billing_items.c.billing_id)\
    .join(frames, billing_items.c.frame_id == frames.c.id)\
    .join(lenses, billing_items.c.lens_id == lenses.c.id)\
    .join(payment_details, billings.c.id == payment_details.c.billing_id)\
    .filter(customers.c.branch_id == branch_id).all()

    # If no results found, raise an HTTPException
    if not query_result:
        raise HTTPException(status_code=404, detail="No billing details found for the provided branch ID")

    # Convert the query result to a list of dictionaries for serialization
    formatted_result = [
        {
            "invoice_date": row.invoice_date,
            "customer_name": row.customer_name,
            "mobile_number": row.mobile_number,
            "sales_person": row.sales_person,
            "lens_category": row.lens_category,
            "frame_brand": row.frame_brand,
            "advance_paid": row.advance_paid,
            "grand_total": row.grand_total,
            "balance_amount": row.balance_amount,
            "pay_type": row.pay_type
        }
        for row in query_result
    ]

    # Return the formatted result
    return formatted_result

@router.get("/monthly-sales")
async def get_monthly_sales(db: Session = Depends(get_db)):
    monthly_sales = db.query(
        extract('year', billings.c.invoice_date).label("year"),
        extract('month', billings.c.invoice_date).label("month"),
        func.sum(payment_details.c.grand_total).label("total_sales")
    ).join(
        payment_details, billings.c.id == payment_details.c.billing_id
    ).group_by(
        "year", "month"
    ).order_by(
        "year", "month"
    ).all()

    if not monthly_sales:
        raise HTTPException(status_code=404, detail="No sales data found")

    formatted_sales = [
        {
            "year": year,
            "month": month,
            "total_sales": total_sales
        } for year, month, total_sales in monthly_sales
    ]

    return formatted_sales

# monly grand total

@router.get("/current-monthly-sales/{branch_id}")
async def get_current_monthly_sales(branch_id: int, db: Session = Depends(get_db)):
    # Automatically detect the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    total_sales = db.query(
        func.sum(payment_details.c.grand_total).label("total_sales")
    ).join(
        billings, payment_details.c.billing_id == billings.c.id
    ).join(
        customers, billings.c.customer_id == customers.c.id
    ).filter(
        customers.c.branch_id == branch_id,
        extract('year', billings.c.invoice_date) == current_year,
        extract('month', billings.c.invoice_date) == current_month
    ).scalar()

    if total_sales is None:
        raise HTTPException(status_code=404, detail=f"No sales data found for branch ID {branch_id} in {current_month}/{current_year}")

    return {
        "branch_id": branch_id,
        "year": current_year,
        "month": current_month,
        "total_sales": float(total_sales) if total_sales else 0.0
    }

# todays orders

@router.get("/daily-orders/{branch_id}")
async def get_daily_orders(
    branch_id: int, 
    order_date: str = Query(...),  # Expecting a date in 'YYYY-MM-DD' format as a query parameter
    db: Session = Depends(get_db)
):
    # Parse the input date string to a date object
    try:
        order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

    order_count_result = db.query(func.count(billings.c.id)).join(
        customers, billings.c.customer_id == customers.c.id
    ).filter(
        customers.c.branch_id == branch_id,
        func.date(billings.c.invoice_date) == order_date
    ).scalar()

    order_count = 0 if order_count_result is None else order_count_result

    return {
        "branch_id": branch_id,
        "date": order_date.isoformat(),
        "order_count": order_count
    }

# total total of sale

@router.get("/total-sales/{branch_id}")
async def get_total_sales(
    branch_id: int, 
    sales_date: str = Query(...),  # Use a Query parameter to accept the date in 'YYYY-MM-DD' format
    db: Session = Depends(get_db)):
    # Parse the input sales_date string to a date object
    try:
        # Ensure the sales_date is in 'YYYY-MM-DD' format
        parsed_sales_date = datetime.strptime(sales_date, "%Y-%m-%d").date()
    except ValueError:
        # If there's an error in parsing, return an error message
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

    total_sales = db.query(
        func.sum(payment_details.c.grand_total).label("total_sales")
    ).join(
        billings, payment_details.c.billing_id == billings.c.id
    ).join(
        customers, billings.c.customer_id == customers.c.id
    ).filter(
        customers.c.branch_id == branch_id,
        func.date(billings.c.invoice_date) == parsed_sales_date  # Use the parsed date in the filter
    ).scalar()

    # If there are no sales, set total_sales to 0.0
    if total_sales is None:
        total_sales = 0.0

    return {
        "branch_id": branch_id,
        "date": parsed_sales_date.isoformat(),
        "total_sales": total_sales
    }

#count of totay customers

@router.get("/unique-customers/{branch_id}")
async def get_unique_customers(
    branch_id: int, 
    sales_date: str = Query(...),  # Accept the date in 'YYYY-MM-DD' format as a query parameter
    db: Session = Depends(get_db)):
    # Parse the input sales_date string to a date object
    try:
        # Ensure the sales_date is in 'YYYY-MM-DD' format
        parsed_sales_date = datetime.strptime(sales_date, "%Y-%m-%d").date()
    except ValueError:
        # If there's an error in parsing, return an error message
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

    unique_customers_count = db.query(
        func.count(distinct(billings.c.customer_id))
    ).join(
        customers, billings.c.customer_id == customers.c.id
    ).filter(
        customers.c.branch_id == branch_id,
        func.date(billings.c.invoice_date) == parsed_sales_date  # Use the parsed date in the filter
    ).scalar()

    # If no unique customers are found, default to 0
    unique_customers_count = unique_customers_count or 0

    return {
        "branch_id": branch_id,
        "date": parsed_sales_date.isoformat(),
        "unique_customers_count": unique_customers_count
    }