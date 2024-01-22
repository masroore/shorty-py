import url_normalize
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from src import models, schemas, crud
from src.config import get_settings
from src.db import get_db, create_tables

app = FastAPI()
create_tables()


def get_admin_info(db_url: models.Link) -> schemas.LinkInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def raise_not_found(request: Request):
    raise HTTPException(status_code=404, detail=f"URL '{request.url}' doesn't exist")


@app.post("/url", response_model=schemas.LinkInfo)
def create_url(
    url: schemas.LinkBase,
    db: Session = Depends(get_db),
):
    # if not validators.url(url.target_url): raise HTTPException(status_code=400, detail="Your provided URL is not valid")
    url.target_url = url_normalize.url_normalize(url.target_url)
    db_url = crud.get_link_by_url(db=db, url=url.target_url)
    if not db_url:
        db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{short_code}")
def forward_to_target_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    if link := crud.get_link_by_short_code(db=db, short_code=short_code):
        crud.update_db_clicks(db=db, link=link)
        ua_string = request.headers.get("user-agent")
        # ip_addr = request.client.host
        ip_addr = request.headers.get("CF-Connecting-IP")
        crud.register_visit(db=db, link=link, ip_addr=ip_addr, ua_string=ua_string)
        return RedirectResponse(link.target_url)
    else:
        raise_not_found(request)


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.LinkInfo,
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if link := crud.get_link_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(link)
    else:
        raise_not_found(request)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
