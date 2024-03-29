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
    branch_id: int  # Assuming branch_id is mandatory

# Schema for customer response
class CustomerResponse(CustomerCreate):
    id: int  # Include the customer ID
    
    
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
    left_add: Optional[str] = None
    right_add: Optional[str] = None
    right_pd: Optional[str] = None
    left_pd: Optional[str] = None

# Schema for billing creation
class BillingCreate(BaseModel):
    customer_id: int
    invoice_date: date
    delivery_date: Optional[date] = None
    sales_person: Optional[str] = None

# Schema for billing response
class BillingResponse(BillingCreate):
    id: Optional[int] = None

# Schema for creating a billing item
class BillingItemCreate(BaseModel):
    billing_id: int
    lens_id: int
    frame_id: int
    frame_qty: int
    lens_qty: int

# Schema for billing item response
class BillingItemResponse(BillingItemCreate):
    id: Optional[int] = None

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

# Pydantic model for response data
class PaymentDetailResponse(BaseModel):
    id: int
    billing_id: int
    total_amount: float
    discount: Optional[float] = None
    fitting_charges: Optional[float] = None
    grand_total: float
    advance_paid: Optional[float] = None
    balance_amount: Optional[float] = None
    pay_type: Optional[str] = None
