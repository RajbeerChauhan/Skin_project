from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
   

    class Config:
        from_attributes = True
