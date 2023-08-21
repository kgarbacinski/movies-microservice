from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src import schemas
from src.cruds.favourites import add_user_favourite, get_user_favourite
from src.cruds.movie import get_movie_by_id, get_movies_by_name
from src.db.session import Session
from src.utils import get_db

router = APIRouter(prefix="/film")


@router.get(
    "/search",
    tags=["Search"],
    status_code=200,
    response_model=List[schemas.MovieSchemaInternal],
)
def search(name: str, db: Session = Depends(get_db)):
    return list(get_movies_by_name(db, name))


@router.post("/add-favourite", tags=["Add"], status_code=200)
def add(request: schemas.FavouriteSchema, db: Session = Depends(get_db)):
    if get_user_favourite(db, request):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)
    if not get_movie_by_id(db, request.movie_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    add_user_favourite(db, request)
    return request
