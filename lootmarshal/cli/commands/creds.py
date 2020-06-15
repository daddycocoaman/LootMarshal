from lootmarshal.server.routers.creds import parse_lsass
import typer
from pathlib import Path
from pydantic.errors import PathError
from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response, print_bad

creds_app = LootMarshalTyper(help="Interact with creds")


@creds_app.command("lsass")
def parse_lsass(
    path: str = typer.Option(..., "-f", metavar="", help="Path to LSASS dump"),
    store: bool = typer.Option(
        False, "-s", metavar="", help="Save creds to secretclient"
    ),
):
    """
    Parses lsass dump for creds. 
    """
    if not Path(path).is_file():
        print_bad(f"File {path} does not exist!")
    else:
        files = {"dump": open(path, "rb")}
        resp = lmcs.request("POST", f"creds/lsass?store={store}", files=files)
        print_cli_response(resp)
