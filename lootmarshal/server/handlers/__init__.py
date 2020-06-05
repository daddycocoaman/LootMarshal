from abc import ABC, abstractmethod
from fastapi import HTTPException, status

from ...settings.lmsettings import _ENV_FILE

class HandlerContext:

    project: str
    handler = None

    @classmethod
    def setContext(cls, ctx: str) -> str:
        from .handlers import AzureHandler

        _handlers = {"Azure": AzureHandler}
        try:
            cls.handler = _handlers[ctx](_ENV_FILE)
            return "Connection to Azure successful!"
        except Exception as e:
            raise e

    @classmethod
    def verifyHandler(cls) -> bool:
        if not cls.handler:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Handler not implemented. Use connect command!")

class Handler(ABC):

    @abstractmethod
    async def validate(self):
        pass

    @abstractmethod
    async def get_store(self):
        pass

    @abstractmethod
    async def get_secret(self, name):
        """Returns a secret from the handler's secretclient.
        Return Exception if unsuccessful."""
        pass
