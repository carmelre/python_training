from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from python_training.base import Base


def get_engine_and_session(db_path):
    """
    This function instantiates a SQLAlchemy engine and session, and returns them.

    :return: engine, session
    """
    engine = create_engine(db_path, echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    instantiated_session = session()
    return engine, instantiated_session


def create_tables(engine=None, db_path=None):
    """
    Creates all the tables that are part of the mapping.
    If an engine is provided it is used, otherwise a new engine would be created.

    :param engine: The engine that holds the database connection.
    :param db_path: The db that a connection should be established to.
    """
    if engine is None:
        engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)
