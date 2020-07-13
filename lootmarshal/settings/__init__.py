from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from .lmsettings import LootMarshalSettings

__version__ = "0.3.0"

settings_path = Path(__file__).parent
if settings_path.joinpath("dev.env").exists():
    _ENV_FILE = settings_path / "dev.env"
elif settings_path.joinpath("settings.env").exists():
    _ENV_FILE = settings_path / "settings.env"
else:
    exit("ERROR: No environment settings file found")
load_dotenv(_ENV_FILE)

try:
    LMSettings = LootMarshalSettings(_ENV_FILE)
except ValidationError as e:
    exit(e)
