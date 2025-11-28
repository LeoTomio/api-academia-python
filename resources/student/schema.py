from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StudentSchema(BaseModel):
    height: Optional[float]
    weight: Optional[float]
    objective: Optional[str]
    registration_date: datetime = datetime.now()
    person_id: str

    class Config:
        from_attribute: True
