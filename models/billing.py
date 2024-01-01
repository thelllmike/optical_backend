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
    Column("gender", String(20), nullable=True)
)

prescriptions = Table(
    "prescriptions", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", None, ForeignKey("customers.id"), nullable=False),
    Column("right_sph", Float),
    Column("right_cyl", Float),
    Column("right_axis", Integer),
    Column("left_sph", Float),
    Column("left_cyl", Float),
    Column("left_axis", Integer),
    Column("add", Float),
    Column("pd", Float),
    Column("date_prescribed", Date, nullable=False)
)

billings = Table(
    "billings", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", None, ForeignKey("customers.id"), nullable=False),
    Column("invoice_date", Date, nullable=False),
    Column("sales_person", String(100), nullable=True)
)

billing_items = Table(
    "billing_items", metadata,
    Column("id", Integer, primary_key=True),
    Column("billing_id", None, ForeignKey("billings.id"), nullable=False),
    Column("product_type", String(50), nullable=False), # 'frame' or 'lens'
    Column("product_id", Integer, nullable=False), # ID from frames or lenses table
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=False)
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
