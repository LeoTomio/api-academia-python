from pydantic import BaseModel
from typing import Optional


class TeacherCreateSchema(BaseModel):
    person_id: str
    cref: str

    class Config:
        from_attributes = True  


class TeacherUpdateSchema(BaseModel):
    creft: Optional[str] = None

    class Config:
        from_attributes = True  