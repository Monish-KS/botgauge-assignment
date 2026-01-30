from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemCreate(BaseModel):
    key: str
    value: str

class ItemUpdate(BaseModel):
    value: str

class ItemResponse(BaseModel):
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10

class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
