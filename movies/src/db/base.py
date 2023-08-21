# Import all the models, so that Base has them before being
# imported by Alembic
from src.db.base_class import Base  # isort:skip
from src.models import Favourites, Movies  # isort:skip
