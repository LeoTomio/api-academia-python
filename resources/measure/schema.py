from pydantic import BaseModel
from datetime import datetime


class MeasureSchema(BaseModel):
    measure_type: str
    value: float
    measure_data: datetime

    class Config:
        from_attribute: True
