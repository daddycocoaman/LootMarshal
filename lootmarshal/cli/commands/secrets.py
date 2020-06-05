import typer

from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response

secret_app = LootMarshalTyper(help="Interact with secrets")

@secret_app.command()
def get(name: str):
    """
    Gets a secret.
    """
    resp = lmcs.request("GET", f"secret/{name}")
    print_cli_response(resp)

@secret_app.command(name="set")
def set_secret(name: str, value: str, content_type: str):
    """
    Sets a secret.
    """
    resp = lmcs.request("POST", f"secret/")
    print_cli_response(resp)