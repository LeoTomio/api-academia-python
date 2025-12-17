from pydantic import BaseModel 
from typing import Optional

class TrainingCreateSchema(BaseModel):
    name: str
    person_id: str

    class Config:
        from_attributes = True  


class TrainingUpdateSchema(BaseModel):
    name: Optional[str]
    person_id: Optional[str]

    class Config:
        from_attributes = True  
