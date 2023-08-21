from _pytest.fixtures import fixture
from fastapi import HTTPException

from src.models import Movies
from tests.fixtures import MockFixture, movies_dict

mock = MockFixture("src.api.admin_views")


class TestAdminSearch:
    URL = "/api/v1/admin/film/search"
    m_get_response_from_OMBD = mock("get_response_from_OMBD")

    @fixture
    def params(self):
        return dict(name="test")

    def test_normal(self, client, params, m_get_response_from_OMBD):
        m_get_response_from_OMBD.return_value = movies_dict
        response = client.get(self.URL, params=params)
        assert response.status_code == 200
        assert response.json() == movies_dict

    def test_not_found(self, client, params, m_get_response_from_OMBD):
        m_get_response_from_OMBD.side_effect = HTTPException(status_code=404)
        response = client.get(self.URL, params=params)
        assert response.json() == {"detail": "Not Found"}
        assert response.status_code == 404


class TestAdminAdd:
    URL = "/api/v1/admin/film/add"
    m_get_response_from_OMBD = mock("get_response_from_OMBD")
    m_get_movie_by_imdbID = mock("get_movie_by_imdbID")
    m_add_movie = mock("add_movie")

    @fixture
    def json(self):
        return dict(imdbID="test")

    def test_normal(
        self,
        client,
        m_get_movie_by_imdbID,
        m_get_response_from_OMBD,
        m_add_movie,
        db,
        json,
    ):
        m_get_movie_by_imdbID.return_value = None
        m_get_response_from_OMBD.return_value = movies_dict
        response = client.post(self.URL, json=json)
        m_add_movie.assert_called_once_with(db, m_get_response_from_OMBD.return_value)
        assert response.status_code == 201
        assert response.json() == movies_dict

    def test_not_found(
        self, client, m_get_response_from_OMBD, json, m_get_movie_by_imdbID
    ):
        m_get_movie_by_imdbID.return_value = None
        m_get_response_from_OMBD.side_effect = HTTPException(status_code=404)
        response = client.post(self.URL, json=json)
        assert response.json() == {"detail": "Not Found"}
        assert response.status_code == 404

    def test_movie_exists(self, client, m_get_movie_by_imdbID, json):
        m_get_movie_by_imdbID.return_value = Movies()
        response = client.post(self.URL, json=json)
        assert response.json() == {"detail": "See Other"}
        assert response.status_code == 303
