# from ....config.environment import get_settings

# import sys
from typing import Callable
# sys.path.append("..")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from server.config.environment import get_settings

settings = get_settings()
database_url = settings.SQLALCHEMY_DATABASE_URL


class SQLAlchemy:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

def _configure_initial_sqlalchemy() -> Callable[[], SQLAlchemy]:
    def fn() -> SQLAlchemy:
        return SQLAlchemy()
    return fn

get_sqlalchemy = _configure_initial_sqlalchemy()