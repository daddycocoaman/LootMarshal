import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from lootmarshal.settings import __version__
from .handlers import HandlerContext as HC
from .routers import connect, secrets, misc

app = FastAPI()
app.include_router(connect.router, prefix="/connect", tags=["connect"])
app.include_router(secrets.router, prefix="/secret", 
                   dependencies=[Depends(HC.verifyHandler)], tags=["secrets"])
app.include_router(misc.router, tags=["utils"])


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
