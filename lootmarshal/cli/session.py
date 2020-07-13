from typing import Text, Union

import click_spinner
import requests
from requests.compat import urljoin
from requests.models import Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from ..settings import LMSettings

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
        cert = (
            (LMSettings.ssl_certfile, LMSettings.ssl_keyfile)
            if LMSettings.ssl
            else None
        )
        url = urljoin(self.base_url, url)
        with click_spinner.spinner():
            return super().request(
                method, url, cert=cert, verify=False, *args, **kwargs
            )
