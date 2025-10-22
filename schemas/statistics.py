from pydantic import BaseModel
from typing import Dict


class StatisticsDetail(BaseModel):
    total_users: int
    new_users_last_30_days: int
    total_hikes: int
    hikes_by_status: Dict[str, int]
    total_applications: int
    applications_by_status: Dict[str, int]
    total_articles: int
    total_news: int
    total_passes: int
