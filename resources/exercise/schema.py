from pydantic import BaseModel
from typing import Optional


class ExerciseCreateSchema(BaseModel):
    name: str
    category_id: str

    class Config:
        from_attributes = True  


class ExerciseUpdateSchema(BaseModel):
    name: Optional[str] = None
    category_id: Optional[str] = None

    class Config:
        from_attributes = True  
