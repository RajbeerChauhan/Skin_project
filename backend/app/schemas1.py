from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email:  str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str
