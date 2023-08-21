from _pytest.fixtures import fixture
from fastapi import status

from tests.api.fixtures import expected_movies_json
from tests.fixtures import MockFixture

mock = MockFixture("src.api.admin.views")


class TestSearchView:
    URL = "api/v1/admin/film/search"
    m_requests_get = mock("requests.get")

    @fixture
    def params(self):
        return dict(name="test")

    def test_authenticated(
        self, client, m_requests_get, m_is_admin_true, cookies, params
    ):
        m_requests_get.return_value.status_code = 200
        m_requests_get.return_value.json.return_value = expected_movies_json
        response = client.get(self.URL, params=params, cookies=cookies)
        assert response.status_code == m_requests_get.return_value.status_code
        assert response.json() == m_requests_get.return_value.json.return_value

    def test_not_authenticated(self, client, params, cookies, m_is_admin_false):
        response = client.get(self.URL, params=params, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


class TestAddFromAPIView:
    URL = "api/v1/admin/film/add"
    m_requests_post = mock("requests.post")

    @fixture
    def cookies(self):
        return dict(access_token="123", refresh_token="123", id_token="123")

    @fixture
    def json(self):
        return dict(imdbID="123")

    def test_authenticated(
        self, client, m_requests_post, m_is_admin_true, cookies, json
    ):
        m_requests_post.return_value.status_code = 200
        m_requests_post.return_value.json.return_value = expected_movies_json
        response = client.post(self.URL, json=json, cookies=cookies)
        assert response.status_code == m_requests_post.return_value.status_code
        assert response.json() == m_requests_post.return_value.json.return_value

    def test_not_authenticated(self, client, json, cookies, m_is_admin_false):
        response = client.post(self.URL, json=json, cookies=cookies)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Unauthorized"}
