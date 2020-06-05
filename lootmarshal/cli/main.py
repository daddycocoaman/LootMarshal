import uvicorn

from ..settings import LMSettings
from .commands import *
from .loottyper import LootMarshalTyper

cli = LootMarshalTyper()
cli.add_typer(connect_app, name="connect")
cli.add_typer(secret_app, name="secret")

@cli.command()
def server():
    """
    Starts the LootMarshal server
    """

    uvicorn.run("lootmarshal.server.main:app", reload=LMSettings.debug, 
                host=str(LMSettings.host), port=LMSettings.port)
