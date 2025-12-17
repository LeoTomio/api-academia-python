from pydantic import BaseModel
from typing import Optional


class PersonCreateSchema(BaseModel):
    name: str
    age: int
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    plan_id: Optional[str] = None

    class Config:
        from_attributes = True  


class PersonUpdateSchema(BaseModel):
    name: str
    age: int
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    plan_id: Optional[str] = None

    class Config:
        from_attributes = True  
