from fastapi import APIRouter
from ..handlers import HandlerContext as HC
from ..models import SecretModel

router = APIRouter()

@router.post("", summary="Stores a secret")
async def create_secret(secret: SecretModel):
    handler = HC.handler
    msg = await handler.add_secret(secret.name, secret.value, secret.content_type)
    return {'msg': msg}

@router.get("/{name}", summary="Gets a secret")
async def get_secret(name: str):
    handler = HC.handler
    msg = await handler.get_secret(name)
    return {'msg': msg}

