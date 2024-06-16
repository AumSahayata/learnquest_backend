from fastapi import FastAPI
from .auth.routes import auth_router
from .course.routes import course_router

app = FastAPI(
    title="LearnQuest",
    description="An online learning platform",
)

app.include_router(auth_router, prefix = f"/api/auth", tags = "auth")
app.include_router(course_router, prefix = f"/api/course", tags= "courses")