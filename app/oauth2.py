#app/oauth2.py
from jose import jwt,JWTError
from datetime import datetime,timedelta
from .config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from app.schemas import TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy import select
from . import models

oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expires_minutes


def create_access_token (data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token


def verify_access_token (token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return TokenData(id = str(user_id))
    except JWTError:
        raise credentials_exception
    
    
async def get_current_user(token:str = Depends(oath2_scheme),db:AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"www-Authenticate":"Bearer"},)
    token_data = verify_access_token(token,credentials_exception)
    stmt =select(models.User).where(models.User.id == int(token_data.id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user