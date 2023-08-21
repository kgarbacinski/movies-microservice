from enum import Enum

import requests
from fastapi import HTTPException, Request

from src.core import config


class SearchType(Enum):
    NAME = "t"
    IMDBID = "i"


def get_db(request: Request):
    return request.state.db


def get_response_from_OMBD(search_value: str, type: SearchType):
    params = {"apikey": config.OMBD_API_KEY, "plot": "full", type.value: search_value}
    response = requests.get(config.OMBD_URL, params=params).json()
    try:
        response["Error"]
    except KeyError:
        response = {k[0].lower() + k[1:]: v for k, v in response.items()}
        return response
    raise HTTPException(status_code=404)
