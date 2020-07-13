from abc import ABC, abstractmethod

from fastapi import HTTPException, status

from ...settings import _ENV_FILE


class HandlerContext:

    project: str
    handler = None

    @classmethod
    def setContext(cls, ctx: str) -> str:
        from .azurehandler import AzureHandler

        _handlers = {"azure": AzureHandler}
        try:
            cls.handler = _handlers[ctx](_ENV_FILE)
            return f"Connection to {ctx} successful!"
        except Exception as e:
            raise e

    @classmethod
    def verifyHandler(cls) -> bool:
        if not cls.handler:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Handler not implemented. Use connect command!",
            )


class Handler(ABC):

    secret_index = []

    @abstractmethod
    async def validate(self):
        pass

    @abstractmethod
    async def build_secret_index(self):
        """Create an dict index of secret tags where key is secret name and values are tuple of tag key/value.
        Should be called with create_task during handler initialization and assigned to handler secret_index property.

        Example: {'name': ('tag1', 'value1')}
        """
        pass

    @abstractmethod
    async def write_file(self, directory: str, name: str, file: bytes):
        """Writes a file to the handler's fileclient.
        Return Exception if unsuccessful."""
        pass

    @abstractmethod
    async def read_secret(self, name: str):
        """Returns a secret from the handler's secretclient.
        Return Exception if unsuccessful."""
        pass

    @abstractmethod
    async def write_secret(self, name: str, value: str, content_type: str, tags: dict):
        """Writes a secret to the handler's secretclient.
        Return Exception if unsuccessful."""
        pass

    @abstractmethod
    async def list_secrets(self):
        """Returns all secrets from the handler's secretclient.
        Return Exception if unsuccessful."""
        pass

    async def search_secret_index(self, search: str):
        return [s for s in self.secret_index if search in str(s)]
