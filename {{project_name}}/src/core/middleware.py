from __future__ import annotations
from typing import TYPE_CHECKING
from starlette.middleware.base import BaseHTTPMiddleware

from core.logger import logger

if TYPE_CHECKING:
    from fastapi import Request


class LogRequests(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"{request.method} {request.url}")
        logger.debug(f"Headers: {dict(request.headers)}")
        response = await call_next(request)
        logger.debug(f"Completed with status {response.status_code}")
        return response
