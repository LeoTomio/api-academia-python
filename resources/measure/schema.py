from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MeasureCreateSchema(BaseModel):
    name:str
    unit:str
    class Config:
        from_attributes = True  
        
class MeasureUpdateSchema(BaseModel):
    name:Optional[str]
    unit:Optional[str]
    class Config:
        from_attributes = True  
