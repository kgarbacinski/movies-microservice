from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from src.db.base_class import Base


class Movies(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    year = Column(Integer)
    released = Column(String)
    runtime = Column(String)
    genre = Column(String)
    director = Column(String)
    writer = Column(String)
    actors = Column(String)
    plot = Column(String)
    language = Column(String)
    country = Column(String)
    awards = Column(String)
    poster = Column(URLType)
    metascore = Column(String)
    imdbRating = Column(Float)
    imdbID = Column(String, unique=True)
    favourites = relationship("Favourites", back_populates="movie")

    def __str__(self) -> str:
        return self.title


class Favourites(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movies", back_populates="favourites")
