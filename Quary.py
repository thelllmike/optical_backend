from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from database import SessionLocal
from models.billing import customers, billings, billing_items, payment_details
from models.model import frames , lenses
router = APIRouter()

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