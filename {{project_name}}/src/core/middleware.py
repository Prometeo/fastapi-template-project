from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from core.logger import logger


class LogRequests(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"{request.method} {request.url}")
        logger.debug(f"Headers: {dict(request.headers)}")
        response = await call_next(request)
        logger.debug(f"Completed with status {response.status_code}")
        return response
