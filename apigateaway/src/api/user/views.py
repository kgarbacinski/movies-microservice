import requests
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.api.user import schemas
from src.core import config
from src.dependencies import check_if_logged_get_user_uuid

router = APIRouter(prefix="/film")


@router.get("/search", tags=["Search"], status_code=200)
def search(name: str, user_id: str = Depends(check_if_logged_get_user_uuid)):
    search_suffix = "/user/film/search"
    response = requests.get(
        config.MOVIES_API_URL + search_suffix, params={"name": name}
    )
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.post("/add-favourite", tags=["Add"], status_code=200)
def add(
    request: schemas.idSchema, user_id: str = Depends(check_if_logged_get_user_uuid)
):
    search_suffix = "/user/film/add-favourite"
    json = dict(movie_id=request.movie_id, user_id=user_id)

    response = requests.post(config.MOVIES_API_URL + search_suffix, json=json)
    return JSONResponse(status_code=response.status_code, content=response.json())
