import uvicorn

from ..settings import LMSettings
from .commands import *
from .loottyper import LootMarshalTyper

cli = LootMarshalTyper()
cli.add_typer(connect_app, name="connect")
cli.add_typer(secret_app, name="secrets")
cli.add_typer(creds_app, name="creds")


@cli.command()
def server():
    """
    Starts the LootMarshal server
    """

    uvicorn.run(
        "lootmarshal.server.main:app",
        reload=LMSettings.debug,
        host=str(LMSettings.host),
        workers=LMSettings.workers,
        port=LMSettings.port,
        ssl_keyfile=LMSettings.ssl_keyfile if LMSettings.ssl else None,
        ssl_certfile=LMSettings.ssl_certfile if LMSettings.ssl else None,
    )
