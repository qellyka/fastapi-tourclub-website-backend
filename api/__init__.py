__all__ = {
    "user_router",
    "hike_router",
    "pass_router",
    "additional_router",
}
from .v1.archive.hike import router as hike_router
from .v1.archive.passage import router as pass_router
from .v1.archive.additional import router as additional_router
from .v1.auth import router as user_router
