from fastapi import APIRouter, Depends, HTTPException, status

from src import schemas
from src.cruds.movie import add_movie, get_movie_by_imdbID
from src.db.session import Session
from src.schemas import imdbIDMovieSchema
from src.utils import SearchType, get_db, get_response_from_OMBD

router = APIRouter(prefix="/film")


@router.get(
    "/search", tags=["Search"], status_code=200, response_model=schemas.MovieSchemaOMBD
)
def search(name: str):
    return get_response_from_OMBD(name, SearchType.NAME)


@router.post(
    "/add", tags=["Add"], status_code=201, response_model=schemas.MovieSchemaOMBD
)
def add_from_api(request: imdbIDMovieSchema, db: Session = Depends(get_db)):
    if not get_movie_by_imdbID(db, request.imdbID):
        response = get_response_from_OMBD(request.imdbID, SearchType.IMDBID)
        movie = schemas.MovieSchemaOMBD(**response)
        add_movie(db, movie)
        return movie
    raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)
