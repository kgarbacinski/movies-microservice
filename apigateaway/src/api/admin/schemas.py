from pydantic import BaseModel


class imdbIDMovie(BaseModel):
    imdbID: str
