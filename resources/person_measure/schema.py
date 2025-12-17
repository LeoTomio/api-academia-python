from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PersonMeasureCreateSchema(BaseModel):
    measure_id: str
    value: float

    class Config:
        from_attributes = True


class PersonMeasureUpdateSchema(BaseModel):
    value: float = None

    class Config:
        from_attributes = True
