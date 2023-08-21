from _pytest.fixtures import fixture

from tests.api.fixtures import expected_movies_json
from tests.fixtures import MockFixture

mock = MockFixture("src.api.admin.views")


class TestSearchView:
    URL = "api/v1/user/film/search"
    m_requests_get = mock("requests.get")

    @fixture
    def params(self):
        return dict(name="test")

    def test_authenticated(
        self, client, m_user_logged, params, m_requests_get, cookies
    ):
        m_requests_get.return_value.status_code = 200
        m_requests_get.return_value.json.return_value = expected_movies_json
        response = client.get(self.URL, params=params, cookies=cookies)
        assert response.status_code == m_requests_get.return_value.status_code
        assert response.json() == m_requests_get.return_value.json.return_value

    def test_not_authenticated(self, client, params, cookies, m_user_not_logged):
        response = client.get(self.URL, params=params, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


class TestAddView:
    URL = "api/v1/user/film/add-favourite"
    m_requests_post = mock("requests.post")

    @fixture
    def json(self):
        return dict(movie_id=1)

    def test_authenticated(self, client, m_user_logged, json, m_requests_post, cookies):
        m_requests_post.return_value.status_code = 200
        m_requests_post.return_value.json.return_value = {"detail": "Ok"}
        response = client.post(self.URL, json=json, cookies=cookies)
        assert response.status_code == m_requests_post.return_value.status_code
        assert response.json() == m_requests_post.return_value.json.return_value

    def test_not_authenticated(self, client, json, cookies, m_user_not_logged):
        response = client.post(self.URL, json=json, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}
