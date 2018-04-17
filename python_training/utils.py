from sqlalchemy.orm import sessionmaker


def get_session(engine):
    """
    Returns a session to the DB which the engine is bound to.
    :param engine: A SQLAlchemy engine.

    :return: A SQLAlchemy session
    """
    session = sessionmaker()
    session.configure(bind=engine)
    return session()
