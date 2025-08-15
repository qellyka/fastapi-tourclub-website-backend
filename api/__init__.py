__all__ = {"user_router", "hike_router"}
from .v1.archive.hike import router as hike_router
from .v1.auth import router as user_router
