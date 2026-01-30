from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)

    def get_client_id(self, request: Request) -> str:
        client_ip = request.client.host if request.client else "unknown"
        return client_ip

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        client_requests = self.requests[client_id]
        client_requests[:] = [req_time for req_time in client_requests if req_time > cutoff]
        
        if len(client_requests) >= self.max_requests:
            retry_after = int((client_requests[0] + timedelta(seconds=self.window_seconds) - now).total_seconds())
            return False, max(1, retry_after)
        
        client_requests.append(now)
        remaining = self.max_requests - len(client_requests)
        return True, remaining

    def check_rate_limit(self, request: Request):
        client_id = self.get_client_id(request)
        allowed, retry_after = self.is_allowed(client_id)
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(retry_after)}
            )

rate_limiter = RateLimiter(max_requests=60, window_seconds=60)
