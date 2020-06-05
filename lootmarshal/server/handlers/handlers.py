from uuid import UUID

from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ClientSecretCredential
from azure.keyvault.secrets.aio import SecretClient
from pydantic import BaseSettings
from pydantic.networks import HttpUrl

from . import Handler

class AzureHandler(Handler):
    class Settings(BaseSettings):
        client_id: UUID
        client_secret: str
        keyvault_url: HttpUrl
        storage_blob_url: HttpUrl
        tenant_id: UUID

    def __init__(self, env_file) -> None:
        self.settings = AzureHandler.Settings(_env_file=env_file)
        self.credential = ClientSecretCredential(
            str(self.settings.tenant_id),
            str(self.settings.client_id),
            self.settings.client_secret,
        )
        # Create Blob and KeyVault Secret Clients
        self.storeclient = BlobServiceClient(
            self.settings.storage_blob_url, self.credential)
        self.secretsclient = SecretClient(
            self.settings.keyvault_url, self.credential)

    async def validate(self) -> bool:
        try:
            [c async for c in self.storeclient.list_containers()]
            [p async for p in self.secretsclient.list_properties_of_secrets()]
            return True
        except Exception as e:
            raise e

    async def get_store(self) -> bool:
        pass

    async def get_secret(self, name) -> dict:
        try:
            return await self.secretsclient.get_secret(name)
        except Exception as e:
            return str(e)
    
    async def add_secret(self, name, value, content_type):
        try:
            return await self.secretsclient.set_secret(name, value, 
                                                       content_type=content_type)
        except Exception as e:
            return str(e)