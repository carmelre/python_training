from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from python_training.config import DB_PATH
from python_training.base import Base


def get_engine_and_session():
    """
    This function instantiates a SQLAlchemy engine and session, and returns them.

    :return: engine, session
    """
    engine = create_engine(DB_PATH, echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    instantiated_session = session()
    return engine, instantiated_session


def create_tables(engine):
    """
    Creates all the tables that are part of the mapping.

    :param engine: The engine through which we communicate with the db.
    """
    Base.metadata.create_all(engine)
