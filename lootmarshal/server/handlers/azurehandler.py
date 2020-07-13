import asyncio
import json
import logging
import time
from uuid import UUID

from azure.identity.aio import ClientSecretCredential
from azure.keyvault.secrets.aio import SecretClient
from azure.storage.file import FileService
from fastapi import HTTPException
from pydantic import BaseSettings
from pydantic.networks import HttpUrl
from pydantic.types import SecretStr

from .handlercontext import Handler


class AzureHandler(Handler):
    class Settings(BaseSettings):
        client_id: UUID
        client_secret: SecretStr
        keyvault_url: HttpUrl
        storage_blob_url: HttpUrl
        tenant_id: UUID
        storage_name: str
        storage_share_name: str
        storage_sas: SecretStr

    def __init__(self, env_file) -> None:
        self.settings = AzureHandler.Settings(_env_file=env_file)
        self.credential = ClientSecretCredential(
            str(self.settings.tenant_id),
            str(self.settings.client_id),
            self.settings.client_secret.get_secret_value(),
        )

        # Create File and KeyVault Secret Clients
        self.secret_index = {}
        self.secretsclient = SecretClient(self.settings.keyvault_url, self.credential)
        self.fileclient = FileService(
            self.settings.storage_name,
            sas_token=self.settings.storage_sas.get_secret_value(),
        )
        try:
            self.fileclient.create_share("lootmarshal")
            self.fileclient.create_directory("lootmarshal", "binary_dumps")

            asyncio.create_task(self.build_secret_index())
        except Exception as e:
            raise e

    async def validate(self) -> bool:
        try:

            if not len(self.fileclient.list_shares(num_results=1)):
                raise Exception(
                    "Azure FileService Client could not list shares! Verify authentication."
                )
            [p async for p in self.secretsclient.list_properties_of_secrets()]
            return True
        except Exception as e:
            raise e

    async def build_secret_index(self):
        while True:
            try:
                self.secret_index = [
                    {"name": p.name, "content_type": p.content_type, "tags": p.tags}
                    async for p in self.secretsclient.list_properties_of_secrets()
                ]
            except Exception as e:
                raise e

            await asyncio.sleep(10)

    def write_file(self, directory: str, name: str, file: bytes):
        name = f"{name}_{time.strftime('%Y%m%d-%H%M%S')}"

        logging.info(f"Writing {name} ({len(file)} bytes) to {directory}/{name}.")
        self.fileclient.create_file_from_bytes(
            self.settings.storage_share_name, directory, name, file
        )

    async def read_secret(self, name) -> dict:
        try:
            secret = await self.secretsclient.get_secret(name)
            formatted = {
                "name": secret.name,
                "value": secret.value,
                "content_type": secret.properties.content_type,
                "tags": secret.properties.tags,
            }
            return formatted
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def write_secret(self, name, value, content_type, tags):
        try:
            return await self.secretsclient.set_secret(
                name, value, content_type=content_type, tags=tags
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def list_secrets(self):
        try:
            secret_list = []
            async for props in self.secretsclient.list_properties_of_secrets():
                secret = await self.secretsclient.get_secret(props.name)
                formatted = {
                    "name": secret.name,
                    "value": secret.value,
                    "content_type": secret.properties.content_type,
                    "tags": secret.properties.tags,
                }
                secret_list.append(formatted)
            return json.dumps(secret_list, indent=4)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
