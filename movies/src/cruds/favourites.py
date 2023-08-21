from src import schemas
from src.db.session import Session
from src.models import Favourites


def get_user_favourite(db: Session, favourite: schemas.FavouriteSchema):
    return (
        db.query(Favourites)
        .filter(
            Favourites.user_id == str(favourite.user_id),
            Favourites.movie_id == favourite.movie_id,
        )
        .first()
    )


def add_user_favourite(db: Session, favourite: schemas.FavouriteSchema):
    model = Favourites(movie_id=favourite.movie_id, user_id=str(favourite.user_id))
    db.add(model)
    db.commit()
