#APP/SCHEMAS.PY
from pydantic import EmailStr,BaseModel, Field
from typing import Optional

# ---------- USER SCHEMAS ----------


class UserBase(BaseModel):
    email:EmailStr
    
class UserCreate(UserBase):
    password:str
    
class UserOut(UserBase):
    email:EmailStr
    id:int
    
    
    class Config:
         from_attributes=True

        
        
# ---------- FEEDBACK SCHEMAS ---------

class FeedbackBase(BaseModel):
    content:str  = Field(..., min_length=5, max_length=500)
    
class FeedbackCreate(FeedbackBase):
   pass

class FeedbackResponse(FeedbackBase):
    id:int 
    user_id:int
    
    class Config:
           from_attributes=True

        
# ----------UpdateFeedback----------
        
        
class FeedbackUpdate(BaseModel):
    content: Optional[str] = None 
    
    class Config:
             from_attributes=True

        
# ---------- Token SCHEMAS ----------
class Token(BaseModel):
    access_token: str      
    token_type: str         


class TokenData(BaseModel):
    id: Optional[str] = None  
