from pydantic import BaseModel
from typing import Optional


class ExerciseCreateSchema(BaseModel):
    name: str
    category_id: str

    class Config:
        from_attribute: True


class ExerciseUpdateSchema(BaseModel):
    name: Optional[str]
    category_id: Optional[str]

    class Config:
        from_attribute: True
