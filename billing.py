# customer.py
import select
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from mysqlx import Session
from sqlalchemy import Engine, insert
from sqlalchemy.exc import SQLAlchemyError
from models.Quary import Customer
from schemas.bil_schemas import BillingItemResponse, BillingResponse, CustomerCreate, CustomerResponse, PrescriptionCreate, BillingCreate, BillingItemCreate, PaymentDetailCreate
from database import engine
from models.billing import customers, prescriptions, billings, billing_items, payment_details
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# def get_db():
#     db = Session(bind=engine)
#     try:
#         yield db
#     finally:
#         db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/customers/by-phone/{phone_number}", response_model=CustomerResponse)
def get_customer_by_phone(phone_number: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.mobile_number == phone_number).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers", response_model=CustomerResponse)
async def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    # Check if customer with the same phone number already exists
    existing_customer = db.query(customers).filter(customers.c.mobile_number == customer_data.mobile_number).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="A customer with this phone number already exists")

    with engine.begin() as connection:
        try:
            # Insert customer into the database
            customer_result = connection.execute(customers.insert().values(**customer_data.dict()))
            customer_id = customer_result.inserted_primary_key[0]
            return {"id": customer_id, **customer_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))


# @router.post("/customers", response_model=CustomerResponse)
# async def create_customer(customer_data: CustomerCreate):
#     with engine.begin() as connection:
#         try:
#             # Insert customer into the database
#             customer_result = connection.execute(customers.insert().values(**customer_data.dict()))
#             customer_id = customer_result.inserted_primary_key[0]
#             return {"id": customer_id, **customer_data.dict()}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))


        
@router.post("/prescriptions", response_model=PrescriptionCreate)
async def create_prescription(prescription_data: PrescriptionCreate = Body(...)):
    # Extract customer_id from the payload
    customer_id = prescription_data.customer_id
    
    # Prepare the data for insertion, now including customer_id directly from the payload
    prescription_values = prescription_data.dict()
    
    # Insert prescription, now using customer_id from the payload
    with engine.begin() as connection:
        try:
            prescription_result = connection.execute(
                prescriptions.insert().values(**prescription_values)
            )
            prescription_id = prescription_result.inserted_primary_key[0]
            return {"id": prescription_id, **prescription_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/billings", response_model=BillingResponse)
async def create_billing(billing_data: BillingCreate):
    with engine.begin() as connection:
        try:
            # Insert billing into the database
            billing_result = connection.execute(billings.insert().values(**billing_data.dict()))
            billing_id = billing_result.inserted_primary_key[0]
            return {"id": billing_id, **billing_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
        


        
@router.post("/billings/items", response_model=BillingItemResponse)
async def create_billing_item(billing_item_data: BillingItemCreate):
    with engine.begin() as connection:
        try:
            # Extract billing_id from the request body
            billing_id = billing_item_data.billing_id

            # Create a dictionary from billing_item_data and remove billing_id if it exists
            billing_item_data_dict = billing_item_data.dict()
            # Keep the billing_id in the response
            billing_item_data_dict_with_id = billing_item_data_dict.copy()
            billing_item_data_dict.pop('billing_id', None)

            # Insert billing item linked to the billing record and get the inserted id
            result = connection.execute(billing_items.insert().values(billing_id=billing_id, **billing_item_data_dict))
            inserted_primary_key = result.inserted_primary_key[0]

            # Return response including the id
            return BillingItemResponse(id=inserted_primary_key, **billing_item_data_dict_with_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))



        
# from fastapi import HTTPException
# from sqlalchemy.exc import SQLAlchemyError

@router.post("/billings/payment-details", response_model=PaymentDetailCreate)
async def create_payment_detail(payment_detail_data: PaymentDetailCreate):
    with engine.begin() as connection:
        try:
            # Convert the input model to a dictionary
            payment_detail_data_dict = payment_detail_data.dict()

            # Execute the insert statement
            payment_detail_result = connection.execute(payment_details.insert().values(**payment_detail_data_dict))
            payment_detail_id = payment_detail_result.inserted_primary_key[0]

            # Prepare the response data, including billing_id
            response_data = payment_detail_data.dict()
            response_data['id'] = payment_detail_id

            # Return the result including the payment_detail_id and billing_id
            return response_data
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))




