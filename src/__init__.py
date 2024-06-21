from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from .auth.utils import decode_token
from .auth.routes import auth_router
from .course.routes import course_router

app = FastAPI(
    title="LearnQuest",
    description="An online learning platform",
)

EXCLUDED_PATHS = ["/api/auth/login", "/api/auth/signup"]

@app.middleware("http")
async def check_token(request: Request, call_next):
    if request.url.path in EXCLUDED_PATHS:
        return await call_next(request)
    
    print(request.url.path)

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
app.include_router(course_router, prefix = f"/api/course", tags= "courses")