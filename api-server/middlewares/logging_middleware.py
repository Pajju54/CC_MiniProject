import time
import json
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from kafka.kafka_producer import send_log_to_kafka


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Record request start time
        start_time = time.time()
        
        # Get request body if available
        request_body: Optional[str] = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                raw_body = await request.body()
                request_body = raw_body.decode()
            except:
                request_body = "<unable to read request body>"

        # Process the request and get response
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error and re-raise
            self._log_request(request, 500, start_time, request_body, str(e))
            raise e

        # Log the successful request
        self._log_request(request, response.status_code, start_time, request_body)
        
        return response

    def _log_request(self, request: Request, status_code: int, start_time: float, 
                     request_body: Optional[str] = None, error: Optional[str] = None):
        # Calculate processing time
        process_time = (time.time() - start_time) * 1000

        # Create log entry
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "endpoint": str(request.url),
            "path": request.url.path,
            "status_code": status_code,
            "response_time_ms": round(process_time, 2),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "request_id": request.headers.get("x-request-id"),
        }

        # Add request body for POST/PUT/PATCH requests
        if request_body:
            log_entry["request_body"] = request_body

        # Add error information if present
        if error:
            log_entry["error"] = error

        send_log_to_kafka(log_entry)
