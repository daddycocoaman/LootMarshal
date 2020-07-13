from typing import List

import typer

from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response, verify_tags

secret_app = LootMarshalTyper(help="Interact with secrets")


@secret_app.command("get")
def read_secret(name: str):
    """
    Gets a secret.
    """
    resp = lmcs.request("GET", f"secrets/{name}")
    print_cli_response(resp, value="_value")


@secret_app.command("set")
def write_secret(
    name: str = typer.Option(..., "-n", metavar="", help="Name of the secret"),
    value: str = typer.Option(..., "-v", metavar="", help="Value of the secret"),
    content_type: str = typer.Option(
        ..., "-c", metavar="", help="Content type of the secret"
    ),
    tags: List[str] = typer.Option(
        {}, "-t", metavar="", help="Comma-separated tag metadata", callback=verify_tags,
    ),
):
    """
    Sets a secret. Tag key/value must be alphanumeric (underscores are allowed).
    """
    body = {"name": name, "value": value, "content_type": content_type, "tags": tags}
    resp = lmcs.request("PUT", f"secrets/{name}", json=body)
    print_cli_response(resp)


@secret_app.command("list")
def list_secrets():
    """
    Lists all secret.
    """
    resp = lmcs.request("GET", "secrets")
    print_cli_response(resp)


@secret_app.command("search")
def search_secrets(value: str):
    """
    Search secret metadata in index.
    """
    resp = lmcs.request("GET", f"secrets/search?value={value}")
    print_cli_response(resp, format="json")
