from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PersonType(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class Person(BaseModel):
    name:str
    age:int
    phone: Optional[str]
    email: Optional[str]    
    type: PersonType
    is_active: Optional[bool]
    