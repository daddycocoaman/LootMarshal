from fastapi import APIRouter
from ..handlers import HandlerContext as HC
from ...settings import TAGS

router = APIRouter()


@router.get("/tags", summary="Gets list of tags")
async def tags_get():
    return TAGS