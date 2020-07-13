from fastapi import APIRouter

from ..handlers.handlercontext import HandlerContext as HC
from ..models import SecretModel

router = APIRouter()


@router.get("/search", summary="Search secret metadata")
async def search_secrets(value: str):
    results = await HC.handler.search_secret_index(value)
    return {"msg": results}


@router.get("/{name}", summary="Gets a secret by name")
async def read_secret(name: str):
    handler = HC.handler
    try:
        msg = await handler.read_secret(name)
        return {"msg": msg}
    except Exception as e:
        raise e


@router.put("/{name}", summary="Stores a secret")
async def write_secret(name: str, secret: SecretModel):
    handler = HC.handler
    msg = await handler.write_secret(
        secret.name, secret.value, secret.content_type, secret.tags
    )
    return {"msg": msg}


@router.get("", summary="Lists all secrets")
async def list_secrets():
    handler = HC.handler
    try:
        msg = await handler.list_secrets()
        return {"msg": msg}
    except Exception as e:
        raise e
