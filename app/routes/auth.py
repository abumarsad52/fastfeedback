# app/routes/auth.py

from fastapi import Depends, APIRouter, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, utils, models, oauth2
from app.database import get_db
from app.exceptions import InvalidCredentials  # ✅ custom exception
from fastapi import HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"] 
)

# -------------------------
# Register User
# -------------------------
@router.post("/register", response_model=schemas.UserOut)
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(models.User).where(models.User.email == email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        # Here you could also make a custom "UserAlreadyExists" exception if you want consistency
        raise HTTPException(
            status_code=409,
            detail=f"The user with this email: {email} already exists"
        )
    
    hashed_password = utils.hash_password(password)
    new_user = models.User(email=email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# -------------------------
# Login User
# -------------------------
@router.post("/login")
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(models.User).where(models.User.email == user_credentials.username)
    )
    user = query.scalar_one_or_none()
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise InvalidCredentials()  # ✅ custom exception

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# Logout User
# -------------------------
@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
