from sqlalchemy import create_engine

from python_training.midas.config import OPERATIONAL_DB

engine = create_engine(OPERATIONAL_DB, echo=True)