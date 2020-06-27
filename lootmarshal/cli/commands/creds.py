import typer
from pathlib import Path
from .. import LMCliSession as lmcs
from ..loottyper import LootMarshalTyper
from ..utils import print_cli_response

creds_app = LootMarshalTyper(help="Run credential modules")


@creds_app.command("lsass")
def parse_lsass(
    path: Path = typer.Option(
        ...,
        "-f",
        metavar="",
        help="Path to LSASS dump",
        exists=True,
        file_okay=True,
        readable=True,
    ),
    store: bool = typer.Option(
        False, "-s", metavar="", help="Save creds to secretclient"
    ),
):
    """
    Parses lsass dump for creds. 
    """
    files = {"upload_file": open(path, "rb")}
    resp = lmcs.request("POST", f"creds/lsass?store={store}", files=files)
    print_cli_response(resp)


@creds_app.command("binparse")
def parse_bin(
    path: Path = typer.Option(
        ...,
        "-f",
        metavar="",
        help="Path to file",
        exists=True,
        file_okay=True,
        readable=True,
    ),
    min_length: int = typer.Option(
        32, "-l", metavar="", help="Min length of strings to parse", show_default=True
    ),
    store: bool = typer.Option(
        False, "-s", metavar="", help="Save creds to secretclient"
    ),
):
    """
    Parses binary files for interesting strings and creds. 
    """
    files = {"upload_file": open(path, "rb")}
    resp = lmcs.request(
        "POST", f"creds/binparse?store={store}&min_length={min_length}", files=files
    )
    print_cli_response(resp, format="list")
