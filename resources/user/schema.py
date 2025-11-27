from pydantic import BaseModel
from resources.person.schema import Person

class UserSchema(BaseModel):
    person: Person
    cpf: str
    password: str
    
    class Config:
        from_attributes = True
        
class LoginSchema(BaseModel):
    cpf:str
    password:str
    
    class Config:
        from_attributes = True