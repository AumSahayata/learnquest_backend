from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from .auth.utils import decode_token
from .auth.routes import auth_router
from .course.routes import course_router
from .content.routes import content_router
from .enrollment.routes import enrollment_router
import re

app = FastAPI(
    title="LearnQuest",
    description="An online learning platform",
)

EXCLUDED_BASE_PATHS = [
    re.compile(r"^/api/auth/login"),
    re.compile(r"^/api/auth/signup"),
    re.compile(r"^/api/course/?$"),
    re.compile(r"^/api/course/[a-zA-Z0-9-]+/?$"),
    re.compile(r"^/api/course/keywords/[a-zA-Z0-9 ]+/?$"),
]

@app.middleware("http")
async def check_token(request: Request, call_next):
    request_path = request.url.path

    if any(pattern.match(request_path) for pattern in EXCLUDED_BASE_PATHS):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            token_data = decode_token(token)
            request.state.user = token_data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    response = await call_next(request)
    return response

app.include_router(auth_router, prefix = f"/api/auth", tags = "auth")
app.include_router(course_router, prefix = f"/api/course", tags = "course")
app.include_router(content_router, prefix = f"/api/content", tags = "content")
app.include_router(enrollment_router,prefix = f"/api/enroll", tags = "enroll")