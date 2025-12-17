from pydantic import BaseModel
from typing import Optional


class PlanCreateSchema(BaseModel):
    name: str
    price: float
    description: str
    duration_months: int

    class Config:
        from_attribute: True


class PlanUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    duration_months: Optional[int] = None

    class Config:
        from_attribute: True
