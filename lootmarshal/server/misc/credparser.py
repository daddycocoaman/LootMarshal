import re

from ..logging import log

_CRED_FILTERS = [
    "access_token",
    "refresh_token",
    "id_token",
    "login.microsoftonline.",
    "ESTSAUTH",
    "ESTSAUTHPERSISTENT",
    "passwd",
]


class CredParser:
    filters = re.compile(f'({"|".join(_CRED_FILTERS)})')

    @staticmethod
    @log()
    def parse_bin(data: bytes, min_length: int):
        found = []
        strings = re.findall(f"[ -~]{{{min_length},}}", data.decode("latin-1"))
        found = [s for s in strings for m in [CredParser.filters.search(s)] if m]
        return list(set(found))
