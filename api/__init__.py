__all__ = {
    "user_router",
    "hike_router",
    "pass_router",
    "additional_router",
    "hike_participant_router",
    "club_participant_router",
    "user_router",
    "auth_router",
    "article_router",
    "news_router",
    "application_router",
    "file_router",
}
from api.v1.hike import router as hike_router
from api.v1.passage import router as pass_router
from api.v1.additional import router as additional_router
from api.v1.auth import router as auth_router
from api.v1.hike_participant import router as hike_participant_router
from api.v1.club_participant import router as club_participant_router
from api.v1.user import router as user_router
from api.v1.news import router as news_router
from api.v1.article import router as article_router
from api.v1.application import router as application_router
from api.v1.files import router as file_router
