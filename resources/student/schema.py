from pydantic import BaseModel
from typing import Optional 
from datetime import datetime

class Student(BaseModel):
    height: Optional[float]
    weight: Optional[float]
    objective: Optional[str]
    registration_date: datetime = datetime.now()
    