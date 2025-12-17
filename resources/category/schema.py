from pydantic import BaseModel
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True  



class CategoryUpdateSchema(BaseModel):
    name: str
    
    class Config:
        from_attributes = True  
