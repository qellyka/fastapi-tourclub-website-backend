__all__ = {
    "user_router",
    "hike_router",
    "pass_router",
    "additional_router",
    "hike_participant_router",
    "club_participant_router",
}
from .v1.archive.hike import router as hike_router
from .v1.archive.passage import router as pass_router
from .v1.archive.additional import router as additional_router
from .v1.user.auth import router as user_router
from .v1.archive.hike_participant import router as hike_participant_router
from .v1.user.club_participant import router as club_participant_router
