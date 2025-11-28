from pydantic import BaseModel
from datetime import datetime


class TrainingPlanSchema(BaseModel):
    training_id: str
    exercise_id: str
    repetitions: int

    class Config:
        from_attribute: True
