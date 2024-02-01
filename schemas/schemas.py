from pydantic import BaseModel, Field
from typing import Optional

class LensCreate(BaseModel):
    category: str
    coating: str
    power: float
    stock: int
    selling_price: float
    cost: float
    branch_id: int  # Added branch_id

class LensUpdate(BaseModel):
    category: Optional[str] = Field(None)
    coating: Optional[str] = Field(None)
    power: Optional[float] = Field(None)
    stock: Optional[int] = Field(None)
    selling_price: Optional[float] = Field(None)
    cost: Optional[float] = Field(None)
    branch_id: Optional[int] = Field(None)  # Added branch_id as optional

class FrameCreate(BaseModel):
    frame: str
    brand: str
    size: str
    stock: int
    model: str
    color: str
    selling_price: float
    wholesale_price: float
    branch_id: int  # Added branch_id

class FrameUpdate(BaseModel):
    frame: Optional[str] = Field(None)
    brand: Optional[str] = Field(None)
    size: Optional[str] = Field(None)
    stock: Optional[int] = Field(None)
    model: Optional[str] = Field(None)
    color: Optional[str] = Field(None)
    selling_price: Optional[float] = Field(None)
    wholesale_price: Optional[float] = Field(None)
    branch_id: Optional[int] = Field(None)  # Added branch_id as optional
