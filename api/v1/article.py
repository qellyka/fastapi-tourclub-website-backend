from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Article"])


@router.get("/article")
async def get_articles():
    pass


@router.post("/article")
async def create_new_article_item():
    pass


@router.get("/article/{article_id}")
async def get_article_item():
    pass


@router.put("/article/{article_id}")
async def update_article_item():
    pass


@router.delete("/article/{article_id}")
async def delete_article_item():
    pass
