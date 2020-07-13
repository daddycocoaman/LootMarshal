from typing import Optional

from pydantic import BaseModel


class SecretModel(BaseModel):
    name: str
    value: str
    content_type: Optional[str] = ...
    tags: Optional[dict]
