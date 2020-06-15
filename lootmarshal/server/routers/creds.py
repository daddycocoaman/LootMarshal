import json
import typer

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.param_functions import Depends
from pypykatz.commons.common import UniversalEncoder
from pypykatz.pypykatz import pypykatz

from ..handlers.handlercontext import HandlerContext as HC

router = APIRouter()


async def checkHandler(store: bool = False):
    if store and not HC.handler:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Cannot store dump because secrets handler does not exist. Use connect command!",
        )
    return store


@router.post("/lsass", summary="Runs pypykatz on lsass dump.")
async def parse_lsass(
    dump: UploadFile = File(...), store: bool = Depends(checkHandler)
):
    """
    Runs pypykatz on an lsass minidump. Returns credentials.

    Set store to True to save credentials via secretshandler.
    """
    cred_types = [
        "credman_creds",
        "dpapi_creds",
        "kerberos_creds",
        "livessp_creds",
        "msv_creds",
        "ssp_creds",
        "tspkg_creds",
        "wdigest_creds",
    ]
    try:
        creds = pypykatz.parse_minidump_bytes(dump.file.read())
        msg = json.dumps(creds, cls=UniversalEncoder, indent=4, sort_keys=True)
    except Exception as e:
        msg = f"{type(e).__name__}: {e.args}"
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=msg
        )

    if store:
        creds_json = json.loads(msg)
        for v in creds_json["logon_sessions"].values():
            for cred in cred_types:
                if v[cred]:
                    domain = v["domainname"].replace(" ", "-")
                    username = v["username"].rstrip("$").replace(" ", "-")
                    name = f'{domain}--{username}--{v["luid"]}--{cred.split("_")[0]}'
                    await HC.handler.write_secret(name, v[cred], cred)
    return {"msg": msg}
