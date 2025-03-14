from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str
    
class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    
    class Config:
        orm_mode = True
        
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    
    class Config:
        orm_mode = True

# class TaskDelete(BaseModel):
#     user_id: int

#     class Config:
#         orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    
    class Config:
        orm_mode = True