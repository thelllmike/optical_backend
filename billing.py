# customer.py
from fastapi import APIRouter, Depends, HTTPException
from mysqlx import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.bil_schemas import CustomerCreate, PrescriptionCreate, BillingCreate, BillingItemCreate, PaymentDetailCreate
from database import engine
from models.billing import customers, prescriptions, billings, billing_items, payment_details

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/customers", response_model=CustomerCreate)
async def create_customer(customer_data: CustomerCreate):
    with engine.begin() as connection:
        try:
            # Insert customer into the database
            customer_result = connection.execute(customers.insert().values(**customer_data.dict()))
            customer_id = customer_result.inserted_primary_key[0]
            return {"id": customer_id, **customer_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/customers/{customer_id}/prescriptions", response_model=PrescriptionCreate)
async def create_prescription(customer_id: int, prescription_data: PrescriptionCreate):
    # Prepare the data for insertion
    prescription_values = prescription_data.dict()
    prescription_values.pop("customer_id", None)  # Remove customer_id if it exists in dict

    # Insert prescription linked to the customer
    with engine.begin() as connection:
        try:
            prescription_result = connection.execute(prescriptions.insert().values(customer_id=customer_id, **prescription_values))
            prescription_id = prescription_result.inserted_primary_key[0]
            return {"id": prescription_id, **prescription_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/billings", response_model=BillingCreate)
async def create_billing(billing_data: BillingCreate):
    with engine.begin() as connection:
        try:
            # Insert billing into the database
            billing_result = connection.execute(billings.insert().values(**billing_data.dict()))
            billing_id = billing_result.inserted_primary_key[0]
            return {"id": billing_id, **billing_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/billings/{billing_id}/items", response_model=BillingItemCreate)
async def create_billing_item(billing_id: int, billing_item_data: BillingItemCreate):
    with engine.begin() as connection:
        try:
            # Create a dictionary from billing_item_data and remove billing_id if it exists
            billing_item_data_dict = billing_item_data.dict()
            billing_item_data_dict.pop('billing_id', None)

            # Insert billing item linked to the billing record
            billing_item_result = connection.execute(billing_items.insert().values(billing_id=billing_id, **billing_item_data_dict))
            billing_item_id = billing_item_result.inserted_primary_key[0]
            return {"id": billing_item_id, **billing_item_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/billings/{billing_id}/payment-details", response_model=PaymentDetailCreate)
async def create_payment_detail(billing_id: int, payment_detail_data: PaymentDetailCreate):
    with engine.begin() as connection:
        try:
            # Create a dictionary from payment_detail_data and remove billing_id if it exists
            payment_detail_data_dict = payment_detail_data.dict()
            payment_detail_data_dict.pop('billing_id', None)

            # Insert payment details linked to the billing record
            payment_detail_result = connection.execute(payment_details.insert().values(billing_id=billing_id, **payment_detail_data_dict))
            payment_detail_id = payment_detail_result.inserted_primary_key[0]
            return {"id": payment_detail_id, **payment_detail_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))


# Additional endpoints for reading, updating, and deleting customers would be added here...
