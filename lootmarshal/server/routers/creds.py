import json

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status
from fastapi.param_functions import Depends
from pypykatz.commons.common import UniversalEncoder
from pypykatz.pypykatz import pypykatz

from ..handlers.handlercontext import HandlerContext as HC
from ..misc.credparser import CredParser

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
    bgtask: BackgroundTasks,
    upload_file: UploadFile = File(...),
    tags: dict = {},
    store: bool = Depends(checkHandler),
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
        lsass_data = upload_file.file.read()
        creds = pypykatz.parse_minidump_bytes(lsass_data)
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
                    await HC.handler.write_secret(name, v[cred], cred, tags)

        bgtask.add_task(
            HC.handler.write_file,
            directory="binary_dumps",
            name=upload_file.filename,
            file=lsass_data,
        )
    return {"msg": msg}


@router.post("/binparse", summary="Parses binary data for credentials")
async def parse_bin(
    bgtask: BackgroundTasks,
    upload_file: UploadFile = File(...),
    min_length: int = 32,
    store: bool = Depends(checkHandler),
):
    bindata = upload_file.file.read()
    results = CredParser.parse_bin(bindata, min_length)
    if store:
        bgtask.add_task(
            HC.handler.write_file,
            directory="binary_dumps",
            name=upload_file.file.name,
            file=bindata,
        )
    return {"msg": results}
