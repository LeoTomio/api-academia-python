from pydantic import BaseModel
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str

    class Config:
        from_attribute: True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str]
    
    class Config:
        from_attribute: True