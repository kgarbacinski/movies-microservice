import requests
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.api.admin import schemas
from src.core import config
from src.dependencies import check_if_admin

router = APIRouter(prefix="/film")


@router.get("/search", tags=["Search"])
def search(name: str, is_admin: bool = Depends(check_if_admin)):
    search_suffix = "/admin/film/search"
    response = requests.get(
        config.MOVIES_API_URL + search_suffix, params={"name": name}
    )
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.post("/add", tags=["Add"])
def add_from_api(imdbID: schemas.imdbIDMovie, is_admin: bool = Depends(check_if_admin)):
    add_suffix = "/admin/film/add"

    response = requests.post(config.MOVIES_API_URL + add_suffix, json=imdbID.dict())
    return JSONResponse(status_code=response.status_code, content=response.json())
