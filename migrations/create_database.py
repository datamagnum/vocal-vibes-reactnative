import sys

sys.path.extend(["./"])

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)
    print("Database Created")
else:
    print("Database Already Exist")
