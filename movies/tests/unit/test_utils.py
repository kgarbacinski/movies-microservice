from _pytest.fixtures import fixture
from _pytest.python_api import raises
from fastapi import HTTPException

from src.utils import SearchType, get_response_from_OMBD
from tests.fixtures import MockFixture

mock = MockFixture("src.utils")


class TestOMBDApi:
    m_requests = mock("requests.get")

    @fixture
    def OMBD_response(self):
        return {
            "Title": "Psy",
            "Year": "1992",
            "Rated": "N/A",
            "Released": "20 Nov 1992",
            "Runtime": "104 min",
            "Genre": "Action, Crime, Drama",
            "Director": "Wladyslaw Pasikowski",
            "Writer": "Wladyslaw Pasikowski",
            "Actors": "Boguslaw Linda, Marek Kondrat, Cezary Pazura",
            "Plot": "In the good old days Franz Maurer and his partners from the secret police used to live like kings. Now, they all must adapt to a new post-communist environment where they are scorned and losing all privileges. Some, like Franz, are like ordinary police fighting against drug dealers. But Franz will soon find out that some of his friends are on the other side.",
            "Language": "Polish, English, German, Russian",
            "Country": "Poland",
            "Awards": "5 wins",
            "Poster": "https://m.media-amazon.com/images/M/MV5BZGQwODdkOTctYWRlNC00ZjcyLWE4ZjctODQxZGVlM2YyMzViXkEyXkFqcGdeQXVyMjMwOTA0Ng@@._V1_SX300.jpg",
            "Ratings": [{"Source": "Internet Movie Database", "Value": "7.6/10"}],
            "Metascore": "N/A",
            "imdbRating": "7.6",
            "imdbVotes": "5,082",
            "imdbID": "tt0105185",
            "Type": "movie",
            "DVD": "27 Mar 2007",
            "BoxOffice": "N/A",
            "Production": "Studio Filmowe Zebra",
            "Website": "N/A",
            "Response": "True",
        }

    @fixture
    def expected_result(self):
        return {
            "title": "Psy",
            "year": "1992",
            "rated": "N/A",
            "released": "20 Nov 1992",
            "runtime": "104 min",
            "genre": "Action, Crime, Drama",
            "director": "Wladyslaw Pasikowski",
            "writer": "Wladyslaw Pasikowski",
            "actors": "Boguslaw Linda, Marek Kondrat, Cezary Pazura",
            "plot": "In the good old days Franz Maurer and his partners from the secret police used to live like kings. Now, they all must adapt to a new post-communist environment where they are scorned and losing all privileges. Some, like Franz, are like ordinary police fighting against drug dealers. But Franz will soon find out that some of his friends are on the other side.",
            "language": "Polish, English, German, Russian",
            "country": "Poland",
            "awards": "5 wins",
            "poster": "https://m.media-amazon.com/images/M/MV5BZGQwODdkOTctYWRlNC00ZjcyLWE4ZjctODQxZGVlM2YyMzViXkEyXkFqcGdeQXVyMjMwOTA0Ng@@._V1_SX300.jpg",
            "ratings": [{"Source": "Internet Movie Database", "Value": "7.6/10"}],
            "metascore": "N/A",
            "imdbRating": "7.6",
            "imdbVotes": "5,082",
            "imdbID": "tt0105185",
            "type": "movie",
            "dVD": "27 Mar 2007",
            "boxOffice": "N/A",
            "production": "Studio Filmowe Zebra",
            "website": "N/A",
            "response": "True",
        }

    @fixture
    def OMBD_not_found(self):
        return {"Response": "False", "Error": "Movie not found!"}

    def test_normal(self, m_requests, OMBD_response, expected_result):
        m_requests.return_value.json.return_value = OMBD_response
        result = get_response_from_OMBD("psy", SearchType.NAME)
        assert result == expected_result

    def test_not_found(self, m_requests, OMBD_not_found, expected_result):
        m_requests.return_value.json.return_value = OMBD_not_found
        with raises(HTTPException):
            get_response_from_OMBD("123", SearchType.IMDBID)
