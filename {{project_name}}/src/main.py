from fastapi import FastAPI
from core.config import config
from core.middleware import LogRequests
from routers import user, auth, health
from fastapi import Request
from core.logger import logger

app = FastAPI(
    title=config.APP_NAME,
    docs_url=None if config.ENV == "production" else "/docs",
    redoc_url=None if config.ENV == "production" else "/redoc",
    openapi_url=None if config.ENV == "production" else "/openapi.json",
)
app.add_middleware(LogRequests)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(health.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.debug(f"Completed with status {response.status_code}")
    return response
