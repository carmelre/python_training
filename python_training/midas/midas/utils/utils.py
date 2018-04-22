from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


@contextmanager
def get_session(engine):
    """
    Returns a session to the DB which the engine is bound to.
    :param engine: A SQLAlchemy engine.

    :return: A SQLAlchemy session
    """
    try:
        session = sessionmaker()
        session.configure(bind=engine)
        activated_session = session()
        yield activated_session
    finally:
        activated_session.close()
