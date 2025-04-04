from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from middlewares.logging_middleware import LoggingMiddleware 


middleware = [
    Middleware(LoggingMiddleware)
]
app = FastAPI(middleware=middleware)


# Models for request validation
class SubmitData(BaseModel):
    title: str
    content: str

@app.get("/ping")
def ping():
    """Health check endpoint"""
    return {"message": "pong", "status": "healthy"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user details by ID"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")
    return {"user_id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@example.com"}

@app.post("/submit")
def submit_data(data: SubmitData):
    """Submit data with validation"""
    return {
        "message": "Data received successfully",
        "data": data.dict()
    }

@app.get("/error")
def trigger_error():
    """Endpoint to test error logging"""
    raise HTTPException(status_code=500, detail="Internal server error simulation")