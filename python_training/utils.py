from python_training.config import DB_PATH
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_engine_and_session():
    """
    This function instantiates a SQLAlchemy engine and session, and returns them.
    :return: engine, session
    """
    engine = create_engine(DB_PATH, echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return engine, session


