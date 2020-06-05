from fastapi import APIRouter, HTTPException, status
from ..handlers import HandlerContext as HC

router = APIRouter()


@router.get("/azure", summary="Initializes Azure handler")
async def connect_azure():
    try:
        msg = HC.setContext("Azure")
        handler = HC.handler
        if await handler.validate():
            return {"msg": msg}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
