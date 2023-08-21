from sqlalchemy import func

from src import models, schemas
from src.db.session import Session
from src.models import Movies


def add_movie(db: Session, movie: schemas.MovieSchemaOMBD):
    obj = models.Movies(**movie.dict())
    db.add(obj)
    db.commit()


def get_movie_by_imdbID(db: Session, imdbID: str):
    return db.query(Movies).where(Movies.imdbID == imdbID).first()


def get_movies_by_name(db: Session, name: str):
    return (
        db.query(Movies)
        .filter(func.lower(Movies.title).contains(func.lower(name)))
        .all()
    )


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Movies).where(Movies.id == movie_id).first()
