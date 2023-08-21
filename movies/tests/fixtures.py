from typing import Any
from unittest.mock import AsyncMock, MagicMock

from pytest import fixture


class Nothing:
    pass


class MockFixture:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, name: str, return_value: Any = Nothing, async_: bool = False):
        def mocking(clsself, mocker):
            if async_:
                mock = mocker.patch(
                    f"{self.prefix}.{name}",
                    new_callable=AsyncMock if async_ else MagicMock,
                )
            else:
                mock = mocker.patch(f"{self.prefix}.{name}")
            if return_value is not Nothing:
                if callable(return_value):
                    mock.return_value = return_value(self, clsself, mocker)
                else:
                    mock.return_value = return_value
                mock.return_value = return_value
            return mock

        return fixture(mocking)


movies_dict = {
    "title": "Psy",
    "year": 1992,
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
    "metascore": "N/A",
    "imdbRating": 7.6,
    "imdbID": "tt0105185",
}

movies_list = [
    {
        "id": 1,
        "title": "Psy",
        "year": 1992,
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
        "metascore": "N/A",
        "imdbRating": 7.6,
        "imdbID": "tt0105185",
    },
    {
        "id": 2,
        "title": "Psy 2: Ostatnia krew",
        "year": 1994,
        "released": "05 Apr 1994",
        "runtime": "100 min",
        "genre": "Action, Crime, Drama",
        "director": "Wladyslaw Pasikowski",
        "writer": "Wladyslaw Pasikowski",
        "actors": "Boguslaw Linda, Cezary Pazura, Artur Zmijewski",
        "plot": "Franz Maurer, a compromised cop, former officer of the criminal department of the Warsaw's police, is released from prison where he was doing time for his brutality and murders. He is awaited by the New, his fellow-policeman. Franz tries to go straight starting hard work in a steel mill. Nevertheless, he must leave the factory as a criminal with an uncertain past when he doesn't join the strike organized by the workers' union. At the same time, a merciless war continues in former Yugoslavia. Wolf and William, two high rank officers, come to Poland in order to organize a network selling and smuggling arms to Yugoslavia by way of Albania. They seek experienced and loyal partners. Franz is not only amenable to the scheme, but he even draws his former partner into the deal. However, security agents are circling them like buzzards...",
        "language": "Polish, Russian, Serbo-Croatian",
        "country": "Poland",
        "awards": "1 win",
        "poster": "https://m.media-amazon.com/images/M/MV5BZDUwYzY4OTktMGI0YS00Nzg4LWI5MDctZGJkYzA1MTZhNDUyXkEyXkFqcGdeQXVyODg0OTM4NTc@._V1_SX300.jpg",
        "metascore": "N/A",
        "imdbRating": 6.8,
        "imdbID": "tt0110908",
    },
]
