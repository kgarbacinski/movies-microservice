from uuid import uuid4

from _pytest.fixtures import fixture

from src.models import Favourites, Movies
from tests.fixtures import MockFixture, movies_list

mock = MockFixture("src.api.user_views")


class TestUserSearch:
    URL = "api/v1/user/film/search"
    m_get_movies_by_name = mock("get_movies_by_name")

    @fixture
    def params(self):
        return dict(name="psy")

    def test_normal(self, client, params, m_get_movies_by_name):
        m_get_movies_by_name.return_value = movies_list
        response = client.get(self.URL, params=params)
        assert response.status_code == 200
        assert response.json() == m_get_movies_by_name.return_value


class TestUserAddFavourite:
    URL = "api/v1/user/film/add-favourite"
    m_get_user_favourite = mock("get_user_favourite")
    m_get_movie_by_id = mock("get_movie_by_id")
    m_add_user_favourite = mock("add_user_favourite")

    @fixture
    def json(self):
        return dict(movie_id=1, user_id=str(uuid4()))

    def test_normal(
        self,
        client,
        json,
        m_get_user_favourite,
        m_get_movie_by_id,
        m_add_user_favourite,
    ):
        m_get_user_favourite.return_value = None
        m_get_movie_by_id.return_value = Movies()
        response = client.post(self.URL, json=json)
        m_add_user_favourite.assert_called_once()
        assert response.status_code == 200
        assert response.json() == json

    def test_user_favourite_exists(self, client, m_get_user_favourite, json):
        m_get_user_favourite.return_value = Favourites()
        response = client.post(self.URL, json=json)
        assert response.status_code == 303
        assert response.json() == {"detail": "See Other"}

    def test_movie_not_found(
        self, client, json, m_get_user_favourite, m_get_movie_by_id
    ):
        m_get_user_favourite.return_value = None
        m_get_movie_by_id.return_value = None
        response = client.post(self.URL, json=json)
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}
