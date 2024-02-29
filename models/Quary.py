from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Transaction(BaseModel):
    customer_name: str
    mobile_number: str
    invoice_date: str  # Adjust types as needed
    sales_person: str
    frame_bought: str
    lens_bought: str
    advance_paid: float
    grand_total: float
    balance_amount: float
    pay_type: str

class Frame(Base):
    __tablename__ = 'frames'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Lens(Base):
    __tablename__ = 'lenses'
    id = Column(Integer, primary_key=True)
    category = Column(String)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    mobile_number = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    nic_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    gender = Column(String(20), nullable=True)
    branch_id = Column(Integer, ForeignKey('branches.id'))
    # Assuming a backref for branch is defined in Branch model
    # prescriptions relationship
    prescriptions = relationship("Prescription", back_populates="customer")
    # billings relationship
    billings = relationship("Billing", back_populates="customer")

class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    right_sph = Column(String)
    right_cyl = Column(String)
    right_axis = Column(String)
    left_sph = Column(String)
    left_cyl = Column(String)
    left_axis = Column(String)
    left_add = Column(String)
    right_add = Column(String)
    # Relationship to Customer
    customer = relationship("Customer", back_populates="prescriptions")

class Billing(Base):
    __tablename__ = 'billings'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    invoice_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=True)
    sales_person = Column(String(100), nullable=True)
    # Relationship to Customer
    customer = relationship("Customer", back_populates="billings")
    # billing_items relationship
    billing_items = relationship("BillingItem", back_populates="billing")

class BillingItem(Base):
    __tablename__ = 'billing_items'
    id = Column(Integer, primary_key=True)
    billing_id = Column(Integer, ForeignKey('billings.id'), nullable=False)
    frame_id = Column(Integer, nullable=False)  # Assuming frame table exists
    lens_id = Column(Integer, nullable=False)  # Assuming lens table exists
    frame_qty = Column(Integer, nullable=False)
    lens_qty = Column(Float, nullable=False)
    # Relationship to Billing
    billing = relationship("Billing", back_populates="billing_items")

class PaymentDetail(Base):
    __tablename__ = 'payment_details'
    id = Column(Integer, primary_key=True)
    billing_id = Column(Integer, ForeignKey('billings.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    discount = Column(Float)
    fitting_charges = Column(Float)
    grand_total = Column(Float, nullable=False)
    advance_paid = Column(Float)
    balance_amount = Column(Float)
    pay_type = Column(String(50))
    # Relationship to Billing
    billing = relationship("Billing", backref="payment_detail")
