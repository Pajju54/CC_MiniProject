from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from middlewares.logging_middleware import LoggingMiddleware

# Register custom middleware for request logging
middleware = [
    Middleware(LoggingMiddleware)
]

# Create FastAPI app with middleware enabled
app = FastAPI(middleware=middleware)


# Pydantic model to validate incoming POST request payload
class SubmitData(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "FastAPI is running! BTW THIS IS HOME PAGE"}


@app.get("/favicon.ico")
async def favicon():
    return ""


@app.get("/ping")
def ping():
    """
    Health check endpoint.
    Returns a simple 'pong' message with status.
    """
    return {"message": "pong", "status": "healthy"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Retrieve user info based on user_id.
    Only allows positive integers.
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")

    return {
        "user_id": user_id,
        "name": f"User{user_id}",
        "email": f"user{user_id}@example.com"
    }


@app.post("/submit")
def submit_data(data: SubmitData):
    """
    Accept and validate structured data from client.
    Responds back with confirmation and echoed data.
    """
    return {
        "message": "Data received successfully",
        "data": data.dict()
    }


@app.get("/error")
def trigger_error():
    """
    Simulates an internal server error for testing middleware logging.
    """
    raise HTTPException(status_code=500, detail="Internal server error simulation")

@app.post("/dataattempt")
def submit_data(data: SubmitData):
    """
    Accept and validate structured data from client.
    Responds back with confirmation and echoed data.
    """
    return {
        "message": "Data sent to be checked",
        "data": data.dict()
    }


@app.get("/version")
def get_version():
    """
    Returns the current version of the API.
    """
    return {
        "version": "1.0.0",
        "description": "Initial release version"
    }


@app.get("/status")
def system_status():
    """
    Returns basic system status.
    """
    return {
        "status": "running",
        "uptime": "72 hours",
        "load": "normal"
    }
