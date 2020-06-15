from typing import Text, Union

import requests
from requests.models import Response
from requests.compat import urljoin
from ..settings import LMSettings


class LootMarshalCliSession(requests.Session):
    def __init__(self) -> None:
        scheme = "https://" if LMSettings.ssl else "http://"
        url = LMSettings.host
        port = LMSettings.port
        self.base_url = f"{scheme}{url}:{port}"
        super().__init__()

    def request(
        self, method: str, url: Union[str, bytes, Text], *args, **kwargs
    ) -> Response:
        url = urljoin(self.base_url, url)
        return super().request(method, url, *args, **kwargs)
