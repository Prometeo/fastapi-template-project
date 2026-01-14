import time

from fastapi import APIRouter


router = APIRouter(tags=["health check"])


@router.get("/health")
async def health_check_endpoint():
    """
    Return the API status.
    This can include checks for database connection, memory usage, etc.
    """
    return {"status": "healthy", "timestamp": time.time()}


@router.get("/readiness", status_code=200)
def readiness_check():
    """
    Readiness probe: Checks if the application is ready to accept traffic.
    This can include checking dependencies like databases, caches, etc.
    """

    # 2. Add other checks (e.g., database connection)
    # try:
    #     db.execute("SELECT 1")
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #         detail="Database not available"
    #     )

    return {"status": "ready", "timestamp": time.time()}
