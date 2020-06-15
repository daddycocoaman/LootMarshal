from pathlib import Path
from pydantic import BaseSettings
from pydantic.class_validators import validator
from pydantic.networks import IPvAnyAddress


class LootMarshalSettings(BaseSettings):
    host: IPvAnyAddress
    port: int
    debug: bool
    ssl: bool
    handler: str

    @validator("port")
    def valid_port(cls, value):
        if not 0 < value <= 65535:
            raise ValueError("Invalid Port! Must be between 1 and 65535.")
        return value

    @validator("handler")
    def valid_handler(cls, value):
        handlers = ["azure"]
        if value.lower() not in handlers:
            raise ValueError(f"Invalid Handler! Must be {handlers}")
        return value
