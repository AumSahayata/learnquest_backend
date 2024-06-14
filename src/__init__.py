from fastapi import FastAPI
from .auth.routes import auth_router

app = FastAPI(
    title="LearnQuest",
    description="An online learning platform",
)

app.include_router(auth_router, prefix = f"/api/auth", tags = "auth")