import uuid

from _pytest.fixtures import fixture

from src import schemas
from src.cruds.favourites import add_user_favourite, get_user_favourite


class TestFavouritesCruds:
    @fixture
    def uuid(self):
        return uuid.uuid4()

    @fixture
    def favourite_schema(self, uuid):
        return schemas.FavouriteSchema(movie_id=1, user_id=uuid)

    @fixture
    def insert_favourite(self, db, insert_movie, favourite_schema):
        add_user_favourite(db, favourite_schema)

    def test_get_user_favourite(self, db, insert_favourite, favourite_schema, uuid):
        favourite = get_user_favourite(db, favourite_schema)
        assert favourite.user_id == str(favourite_schema.user_id)
        assert favourite.movie_id == favourite_schema.movie_id
