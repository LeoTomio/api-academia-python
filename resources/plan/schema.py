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
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]
    duration_months: Optional[int]

    class Config:
        from_attribute: True
