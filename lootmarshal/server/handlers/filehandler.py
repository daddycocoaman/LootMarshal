import json
import sqlite3
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseSettings, validator

from .handlercontext import Handler


class FileHandler(Handler):
    class Settings(BaseSettings):
        loot_dir: Path

        @validator("loot_dir")
        def check_loot_dir(cls, value: Path):
            try:
                if str(value).startswith("~"):
                    value = value.expanduser()

                if not value.exists():
                    value.mkdir(parents=True)
            except Exception as e:
                raise e

            return value

    def __init__(self, env_file) -> None:
        self.settings = FileHandler.Settings(_env_file=env_file)
        self.loot_dir = str(self.settings.loot_dir)

        # Create/verify sqlite tables
        self.sqlitecon = sqlite3.connect(
            f"{self.loot_dir}/secrets.db", check_same_thread=False
        )
        c = self.sqlitecon.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS secrets 
                     (name STRING PRIMARY KEY,
                      value STRING
                      content_type STRING)"""
        )
        c.close()

    async def validate(self) -> bool:
        try:
            return True
        except Exception as e:
            raise e

    async def get_store(self) -> bool:
        pass

    async def read_secret(self, name) -> dict:
        try:
            return await self.secretsclient.get_secret(name)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def write_secret(self, name, value, content_type):
        try:
            return await self.secretsclient.set_secret(
                name, value, content_type=content_type
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
                }
                secret_list.append(formatted)
            return json.dumps(secret_list, indent=4)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
