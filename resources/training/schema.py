from pydantic import BaseModel
from datetime import datetime


class TrainingSchema(BaseModel):
    name: str
    person_id: str

    class Config:
        from_attribute: True
