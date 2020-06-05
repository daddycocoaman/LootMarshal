from pydantic import ValidationError
from .lmsettings import LootMarshalSettings
from .tags import TAGS

__version__ = "0.1.0"

try:
    LMSettings = LootMarshalSettings()
except ValidationError as e:
    exit(e)

