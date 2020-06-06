import typer

from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response

secret_app = LootMarshalTyper(help="Interact with secrets")

@secret_app.command("get")
def read_secret(name: str):
    """
    Gets a secret.
    """
    resp = lmcs.request("GET", f"secret/{name}")
    print_cli_response(resp, value="_value")

@secret_app.command("set")
def write_secret(name: str = typer.Option(..., "-n", metavar="", help="Name of the secret"), 
               value: str = typer.Option(..., "-v", metavar="", help="Value of the secret"), 
               content_type: str = typer.Option(..., "-c", metavar="", help="Content type of the secret")):
    """
    Sets a secret.
    """
    body = {'name': name, 'value': value, 'content_type': content_type}
    resp = lmcs.request("PUT", f"secret", json=body)
    print_cli_response(resp)

@secret_app.command("list")
def list_secrets():
    """
    Lists all secret.
    """
    resp = lmcs.request("GET", f"secret")
    print_cli_response(resp)