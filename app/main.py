# app/main.py

from fastapi import FastAPI
from . import models
from .database import engine
from .routes import auth, feedback
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow frontend or any client to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein yahan apne domain ka URL daalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables on startup
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# ✅ Include routers for API endpoints
app.include_router(auth.router)
app.include_router(feedback.router)
