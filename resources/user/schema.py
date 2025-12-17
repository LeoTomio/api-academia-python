from pydantic import BaseModel
from resources.person.schema import PersonCreateSchema

class UserSchema(BaseModel):
    person: PersonCreateSchema
    cpf: str
    password: str
    
    class Config:
        from_attributes = True  
        
class LoginSchema(BaseModel):
    cpf:str
    password:str
    
    class Config:
        from_attributes = True  