import time
import json
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from kafka.kafka_producer import send_log_to_kafka


# Custom logging middleware to intercept and log all incoming HTTP requests
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Record request start time to calculate response time later
        start_time = time.time()
        
        # Initialize request_body to None (only relevant for write operations)
        request_body: Optional[str] = None

        # For methods with a body, try to decode and store the body
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                raw_body = await request.body()
                request_body = raw_body.decode()
            except:
                request_body = "<unable to read request body>"

        # Try forwarding the request to the next handler (FastAPI route)
        try:
            response = await call_next(request)
        except Exception as e:
            # If an error occurs, log it and re-raise to let FastAPI handle the exception
            self._log_request(
                request=request,
                status_code=500,
                start_time=start_time,
                request_body=request_body,
                error=str(e)
            )
            raise e

        # Log successful request after getting the response
        self._log_request(
            request=request,
            status_code=response.status_code,
            start_time=start_time,
            request_body=request_body
        )
        
        return response

    # Internal method to assemble and send the log to Kafka
    def _log_request(
        self,
        request: Request,
        status_code: int,
        start_time: float,
        request_body: Optional[str] = None,
        error: Optional[str] = None
    ):
        # Calculate how long the request took
        process_time = (time.time() - start_time) * 1000  # in milliseconds

        # Compose the log entry
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "endpoint": str(request.url),
            "path": request.url.path,
            "status_code": status_code,
            "response_time_ms": round(process_time, 2),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "request_id": request.headers.get("x-request-id"),  # for tracing, if set by client
        }

        # Include the request body if applicable
        if request_body:
            log_entry["request_body"] = request_body

        # Include the error if one occurred
        if error:
            log_entry["error"] = error

        # Send the log to Kafka
        send_log_to_kafka(log_entry)
