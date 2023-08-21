from pydantic import BaseModel


class idSchema(BaseModel):
    movie_id: int
