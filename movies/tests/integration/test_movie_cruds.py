from _pytest.fixtures import fixture

from src import schemas
from src.cruds.movie import (
    add_movie,
    get_movie_by_id,
    get_movie_by_imdbID,
    get_movies_by_name,
)
from tests.fixtures import movies_dict, movies_list


class TestMovieCruds:
    @fixture
    def insert_movies(self, db):
        for movie in movies_list:
            movie = schemas.MovieSchemaOMBD(**movie)
            add_movie(db, movie)

    def test_get_movie_by_imdbID(self, db, insert_movie):
        movie = insert_movie
        db_movie = get_movie_by_imdbID(db, movie.imdbID).__dict__
        assert "id" in db_movie
        for key, value in movies_dict.items():
            assert db_movie[key] == value

    def test_get_movie_by_id(self, db, insert_movie):
        db_movie = get_movie_by_id(db, 1).__dict__
        assert "id" in db_movie
        for key, value in movies_dict.items():
            assert db_movie[key] == value

    def test_get_movies_list_by_name(self, db, insert_movies):
        db_movies = [movie.__dict__ for movie in get_movies_by_name(db, "psy")]
        for movie in db_movies:
            movie.pop("_sa_instance_state")
        assert db_movies == movies_list
