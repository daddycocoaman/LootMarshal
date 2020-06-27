from pydantic import BaseModel


class SecretModel(BaseModel):
    name: str
    value: str
    content_type: str
    tags: dict = {}
