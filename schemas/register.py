# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# OpticalShop Schemas
class OpticalShopCreate(BaseModel):
    shop_name: str
    head_office_address: Optional[str] = None
    contact_number: Optional[str] = None
    email: EmailStr

class OpticalShopUpdate(BaseModel):
    shop_name: Optional[str] = None
    head_office_address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None

# Branch Schemas
class BranchCreate(BaseModel):
    shop_id: int
    branch_name: str
    branch_code: str
    mobile_number: Optional[str] = None  # Add this line

class BranchUpdate(BaseModel):
    shop_id: Optional[int] = None
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    mobile_number: Optional[str] = None  # Add this line

class BranchDetail(BaseModel):
    branch_name: str
    mobile_number: Optional[str] = None

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    branch_id: int
    role: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    branch_id: Optional[int] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str