from pydantic import BaseModel,model_validator
from typing import Optional


class StudentCreateSchema(BaseModel):
    objective: Optional[str] = None
    teacher_id: Optional[str] = None
    person_id: str

    class Config:
        from_attributes = True
         


class StudentUpdateSchema(BaseModel):
    objective: Optional[str] = None
    teacher_id: Optional[str] = None

    class Config:
        from_attributes = True
