import typer

from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response

connect_app = LootMarshalTyper(help="Connects to a specified handler")

@connect_app.command()
def azure(ctx: typer.Context):
    """
    Connects to Azure.
    """
    resp = lmcs.request("GET", "connect/azure")
    print_cli_response(resp)
