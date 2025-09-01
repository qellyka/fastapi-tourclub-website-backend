from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["News"])


@router.get("/news")
async def get_news():
    pass


@router.post("/news")
async def create_new_news_item():
    pass


@router.get("/news/{news_id}")
async def get_news_item():
    pass


@router.put("/news/{news_id}")
async def update_news_item():
    pass


@router.delete("/news/{news_id}")
async def delete_news_item():
    pass
