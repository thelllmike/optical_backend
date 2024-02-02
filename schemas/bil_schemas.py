from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Schema for creating a new customer
class CustomerCreate(BaseModel):
    mobile_number: str
    full_name: str
    nic_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    branch_id: int  # Assuming branch_id will be provided and is mandatory

# Schema for updating an existing customer
class CustomerUpdate(BaseModel):
    mobile_number: Optional[str] = None
    full_name: Optional[str] = None
    nic_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    branch_id: Optional[int] = None  

# Schema for creating a new prescription
class PrescriptionCreate(BaseModel):
    customer_id: int
    right_sph: Optional[str] = None
    right_cyl: Optional[str] = None
    right_axis: Optional[str] = None
    left_sph: Optional[str] = None
    left_cyl: Optional[str] = None
    left_axis: Optional[str] = None
    add: Optional[str] = None
    pd: Optional[str] = None
    date_prescribed: date

# Schema for billing creation

class BillingCreate(BaseModel):
    customer_id: int
    invoice_date: date
    delivery_date: Optional[date] = None  # Add this line for delivery_date
    sales_person: Optional[str] = None
# Schema for creating a billing item
class BillingItemCreate(BaseModel):
    billing_id: int
    # lens: str
    # frame: str  # 'frame' or 'lens'
    lens_id: int
    frame_id: int  # ID from frames or lenses table
    quantity: int
    unit_price: float

# Schema for payment details creation
class PaymentDetailCreate(BaseModel):
    billing_id: int
    total_amount: float
    discount: Optional[float] = None
    fitting_charges: Optional[float] = None
    grand_total: float
    advance_paid: Optional[float] = None
    balance_amount: Optional[float] = None
    pay_type: Optional[str] = None  # E.g., 'cash', 'credit card', 'check'

# Schemas for updates can be created similarly to how LensUpdate and FrameUpdate are defined,
# with all fields being optional and defaulting to None.

# Additional read schemas can also be defined to reflect the structure of the data when it is being retrieved from the database.
