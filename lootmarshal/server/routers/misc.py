from fastapi import APIRouter
from ...settings import TAGS

router = APIRouter()


@router.get("/tags", summary="Gets list of tags", include_in_schema=False)
async def tags_get():
    return TAGS
