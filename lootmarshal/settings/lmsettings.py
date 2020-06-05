from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv
from pydantic.class_validators import validator
from pydantic.networks import IPvAnyAddress

settings_path = Path(__file__).parent
if settings_path.joinpath("dev.env").exists():
    _ENV_FILE = settings_path / "dev.env"
elif settings_path.joinpath("settings.env").exists():
    _ENV_FILE = settings_path / "settings.env"
else:
    exit("ERROR: No environment settings file found")
load_dotenv(_ENV_FILE)

class LootMarshalSettings(BaseSettings):
    host: IPvAnyAddress
    port: int
    debug: bool
    ssl: bool
    
    class Config:
        _env_file = _ENV_FILE

    @validator('port')
    def valid_port(cls, value):
        if not 0 < value <= 65535:
            raise ValueError("Invalid Port! Must be between 1 and 65535.")
        return value