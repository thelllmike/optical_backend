# customer.py
from fastapi import APIRouter, Body, Depends, HTTPException
from mysqlx import Session
from sqlalchemy import Engine, insert
from sqlalchemy.exc import SQLAlchemyError
from schemas.bil_schemas import BillingItemResponse, BillingResponse, CustomerCreate, CustomerResponse, PrescriptionCreate, BillingCreate, BillingItemCreate, PaymentDetailCreate
from database import engine
from models.billing import customers, prescriptions, billings, billing_items, payment_details
from sqlalchemy.ext.asyncio import AsyncSession

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse)
async def create_customer(customer_data: CustomerCreate):
    with engine.begin() as connection:
        try:
            # Insert customer into the database
            customer_result = connection.execute(customers.insert().values(**customer_data.dict()))
            customer_id = customer_result.inserted_primary_key[0]
            return {"id": customer_id, **customer_data.dict()}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))


        
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
        
# def get_engine():
#     # Return the engine instance here
#     return engine

# @router.post("/billings", response_model=BillingCreate)
# async def create_billing(billing_data: BillingCreate, engine: Engine = Depends(get_engine)):
#     with engine.begin() as connection:
#         try:
#             # Insert billing into the database
#             billing_result = connection.execute(insert(billings).values(**billing_data.dict()))
#             billing_id = billing_result.inserted_primary_key[0]
#             return {"id": billing_id, **billing_data.dict()}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))


        
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


        
# @router.post("/billings/items", response_model=BillingItemCreate)
# async def create_billing_item(billing_id: int, billing_item_data: BillingItemCreate):
#     with engine.begin() as connection:
#         try:
#             # Create a dictionary from billing_item_data and remove billing_id if it exists
#             billing_item_data_dict = billing_item_data.dict()
#             billing_item_data_dict.pop('billing_id', None)

#             # Insert billing item linked to the billing record
#             billing_item_result = connection.execute(billing_items.insert().values(billing_id=billing_id, **billing_item_data_dict))
#             billing_item_id = billing_item_result.inserted_primary_key[0]
#             return {"id": billing_item_id, **billing_item_data_dict}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))


    #/billing/billings/items  
# @router.post("/billings/items", response_model=BillingItemCreate)
# async def create_billing_item(billing_item_data: BillingItemCreate = Body(...)):
#     async with AsyncSession(engine) as session:
#         async with session.begin():
#             try:
#                 # Prepare billing_item_data for insertion
#                 billing_item_data_dict = billing_item_data.dict()

#                 # Insert the billing item into the database, using the provided billing_id
#                 billing_item_result = await session.execute(
#                     billing_items.insert().values(**billing_item_data_dict)
#                 )
#                 await session.commit()

#                 billing_item_id = billing_item_result.inserted_primary_key[0]
#                 return {"id": billing_item_id, **billing_item_data.dict()}
#             except SQLAlchemyError as e:
#                 await session.rollback()
#                 raise HTTPException(status_code=500, detail=str(e))
        


# @router.post("/billings/payment-details", response_model=PaymentDetailCreate)
# async def create_payment_detail(billing_id: int, payment_detail_data: PaymentDetailCreate):
#     with engine.begin() as connection:
#         try:
#             # Create a dictionary from payment_detail_data and remove billing_id if it exists
#             payment_detail_data_dict = payment_detail_data.dict()
#             payment_detail_data_dict.pop('billing_id', None)

#             # Insert payment details linked to the billing record
#             payment_detail_result = connection.execute(payment_details.insert().values(billing_id=billing_id, **payment_detail_data_dict))
#             payment_detail_id = payment_detail_result.inserted_primary_key[0]
#             return {"id": payment_detail_id, **payment_detail_data.dict()}
#         except SQLAlchemyError as e:
#             raise HTTPException(status_code=500, detail=str(e))
            
@router.post("/billings/payment-details", response_model=PaymentDetailCreate)
async def create_payment_detail(payment_detail_data: PaymentDetailCreate = Body(...)):
    async with AsyncSession(engine) as session:
        async with session.begin():
            try:
                # Prepare payment_detail_data for insertion
                payment_detail_data_dict = payment_detail_data.dict()

                # Insert payment details into the database, using the provided billing_id
                payment_detail_result = await session.execute(
                    payment_details.insert().values(**payment_detail_data_dict)
                )
                await session.commit()

                payment_detail_id = payment_detail_result.inserted_primary_key[0]
                return {"id": payment_detail_id, **payment_detail_data.dict()}
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=str(e))


# Additional endpoints for reading, updating, and deleting customers would be added here...
