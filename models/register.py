# models/model.py
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, ForeignKey, Text

metadata = MetaData()

# Updated Optical Shops table definition
optical_shops = Table(
    "optical_shops", metadata,
    Column("id", Integer, primary_key=True),
    Column("shop_name", String(255), nullable=False, unique=True),
    Column("head_office_address", Text),
    Column("contact_number", String(45)),
    Column("email", String(255), unique=True)  # Added email column
)

# Assuming you already have a branches table
branches = Table(
    "branches", metadata,
    Column("id", Integer, primary_key=True),
    Column("branch_name", String(255)),
    Column("branch_code", String(255), unique=True),
    Column("shop_id", Integer, ForeignKey("optical_shops.id")),
    Column("mobile_number", String(45)),
    # ... other columns as needed
)

# Define the users table
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), unique=True),
    Column("password", String(255)),
    Column("role", String(50)),  # New column for user role
    Column("branch_id", Integer, ForeignKey("branches.id"))
    # Add any other fields as needed
)
