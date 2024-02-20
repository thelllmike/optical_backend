# models/model.py
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, ForeignKey, Date

metadata = MetaData()


customers = Table(
    "customers", metadata,
    Column("id", Integer, primary_key=True),
    Column("mobile_number", String(50), nullable=False),
    Column("full_name", String(100), nullable=False),
    Column("nic_number", String(20), nullable=True),
    Column("address", String(255), nullable=True),
    Column("gender", String(20), nullable=True),
    Column("branch_id", Integer, ForeignKey('branches.id')) # Assuming you have a branches table
)

prescriptions = Table(
    "prescriptions", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", None, ForeignKey("customers.id"), nullable=False),
    Column("right_sph", String),
    Column("right_cyl", String),
    Column("right_axis", String),
    Column("left_sph", String),
    Column("left_cyl", String),
    Column("left_axis", String),
    Column("left_add", String),
    Column("right_add", String),
  
)

billings = Table(
    "billings", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False),
    Column("invoice_date", Date, nullable=False),
    Column("delivery_date", Date, nullable=True),  # Add this line for delivery_date
    Column("sales_person", String(100), nullable=True)
)

billing_items = Table(
    "billing_items", metadata,
    Column("id", Integer, primary_key=True),
    Column("billing_id", None, ForeignKey("billings.id"), nullable=False),
    # Column("frame", String(50), nullable=False),
    # Column("lens", String(50), nullable=False),
    Column("frame_id", Integer, nullable=False), # 'frame' or 'lens'
    Column("lens_id", Integer, nullable=False), # ID from frames or lenses table
    Column("frame_qty", Integer, nullable=False),
    Column("lens_qty", Float, nullable=False)
)

payment_details = Table(
    "payment_details", metadata,
    Column("id", Integer, primary_key=True),
    Column("billing_id", None, ForeignKey("billings.id"), nullable=False),
    Column("total_amount", Float, nullable=False),
    Column("discount", Float),
    Column("fitting_charges", Float),
    Column("grand_total", Float, nullable=False),
    Column("advance_paid", Float),
    Column("balance_amount", Float),
    Column("pay_type", String(50)) # E.g., 'cash', 'credit card', 'check'
)
