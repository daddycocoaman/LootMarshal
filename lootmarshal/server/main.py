import logging
import random
import string
import sys
import time
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from lootmarshal.settings import LMSettings, __version__

from .handlers.handlercontext import HandlerContext as HC
from .logging import InterceptHandler, format_record, logger
from .routers import connect, creds, secrets

app = FastAPI(title="LootMarshal", description="Loot organizer", version=__version__)

# LOGGING SETUP
logging.getLogger().handlers = [InterceptHandler()]
logger.configure(
    handlers=[
        {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
        {
            "sink": Path("~/.lootmarshal/lm.log").expanduser(),
            "level": logging.DEBUG,
            "format": format_record,
        },
    ],
)
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

# ROUTER SETUP
app.include_router(connect.router, prefix="/connect", tags=["connect"])
app.include_router(
    secrets.router,
    prefix="/secrets",
    dependencies=[Depends(HC.verifyHandler)],
    tags=["secrets"],
)
app.include_router(creds.router, prefix="/creds", tags=["creds"])


# CONTEXT SETUP
HC.setContext(LMSettings.handler)

# MIDDLEWARE SETUP
# Based on https://gist.github.com/philippegirard/7cdbec8036561285b5579d8d334b20ba#file-main-py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    logger.info(f"rid={idem} start request {request.method} path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )
    return response


@app.get("/", include_in_schema=False)
async def index():
    """
    Return the main page.
    """
    content = """ <html>
        <head>
            <title>LootMarshal</title>
        </head>
        <body>
            <h1>UI coming probably</h1>
        </body>
    </html>"""
    return HTMLResponse(content)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="LootMarshal", version=__version__, routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
