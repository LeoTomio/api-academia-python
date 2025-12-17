from pydantic import BaseModel
from typing import Optional


class TrainingPlanCreateSchema(BaseModel):
    training_id: str
    exercise_id: str
    repetitions: int

    class Config:
        from_attributes = True


class TrainingPlanUpdateSchema(BaseModel):
    training_id: Optional[str] = None
    exercise_id: Optional[str] = None
    repetitions: Optional[int] = None

    class Config:
        from_attributes = True
