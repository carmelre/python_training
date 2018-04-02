from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from python_training.base import Base


def get_connection(db_path, get_session=False, get_engine=False):
    """
    This function instantiates a SQLAlchemy engine and session, and returns them by demand.

    :param get_engine: Whether an engine object should be returned.
    :param get_session: Whether a session object should be returned.
    :return: session, engine (by demand)
    """
    if get_session is False and get_engine is False:
        raise KeyError('No connection parameter has been requested')
    engine = create_engine(db_path, echo=True)
    if get_engine is True and get_session is False:
        return engine
    session = sessionmaker()
    session.configure(bind=engine)
    instantiated_session = session()
    if get_engine is False and get_session is True:
        return instantiated_session
    return instantiated_session, engine


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
