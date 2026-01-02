from fastapi import APIRouter
from datetime import datetime
### Azure changes
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", summary="Health check")
async def health():
    """Simple health endpoint returning service status and timestamp."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}
 
