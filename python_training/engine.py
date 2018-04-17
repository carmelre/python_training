from python_training.config import OPERATIONAL_DB
from sqlalchemy import create_engine

engine = create_engine(OPERATIONAL_DB, echo=True)