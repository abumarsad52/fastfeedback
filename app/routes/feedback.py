# app/routes/feedback.py

from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app import schemas, models, oauth2
from app.database import get_db
from app.exceptions import FeedbackNotFound  # ✅ import custom exception



router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

# -------------------------
# Create Feedback
# -------------------------
@router.post(
    "/", 
    response_model=schemas.FeedbackResponse, 
    status_code=status.HTTP_201_CREATED)
   
async def create_feedback(
    content: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_feedback = models.Feedback(content=content, user_id=current_user.id)
    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    return new_feedback

# -------------------------
# Get All Feedbacks for User
# -------------------------
@router.get("/", response_model=list[schemas.FeedbackResponse])
async def get_feedbacks(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = (
        select(models.Feedback)
        .where(models.Feedback.user_id == current_user.id)
        .order_by(desc(models.Feedback.created_at))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    feedbacks = result.scalars().all()
    return feedbacks

# -------------------------
# Get Single Feedback by ID
# -------------------------
@router.get("/{id}", response_model=schemas.FeedbackResponse)
async def get_feedback(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    stmt = select(models.Feedback).where(
        (models.Feedback.id == id) & (models.Feedback.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    feedback = result.scalar_one_or_none()
    if feedback is None:
        raise FeedbackNotFound()  # ✅ custom exception used
    return feedback

# -------------------------
# Delete Feedback
# -------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    stmt = select(models.Feedback).where(
        (models.Feedback.id == id) & (models.Feedback.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    feedback = result.scalar_one_or_none()
    if feedback is None:
        raise FeedbackNotFound()  # ✅ custom exception used
    await db.delete(feedback)
    await db.commit()

# -------------------------
# Update Feedback
# -------------------------
@router.put("/{id}", response_model=schemas.FeedbackResponse)
async def update_feedback(
    id: int,
    updated_data: schemas.FeedbackUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    stmt = select(models.Feedback).where(
        (models.Feedback.id == id) & (models.Feedback.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    feedback = result.scalar_one_or_none()

    if feedback is None:
        raise FeedbackNotFound()  # ✅ custom exception used

    data = updated_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(feedback, key, value)

    await db.commit()
    await db.refresh(feedback)
    return feedback
