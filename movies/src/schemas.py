import uuid

from pydantic import AnyUrl, BaseModel


class MovieSchemaOMBD(BaseModel):
    title: str
    year: int
    released: str
    runtime: str
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: AnyUrl
    metascore: str
    imdbRating: float
    imdbID: str

    class Config:
        orm_mode = True


class MovieSchemaInternal(MovieSchemaOMBD):
    id: int


class imdbIDMovieSchema(BaseModel):
    imdbID: str


class FavouriteSchema(BaseModel):
    movie_id: int
    user_id: uuid.UUID

    class Config:
        orm_mode = True
