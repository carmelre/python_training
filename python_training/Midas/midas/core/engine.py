from sqlalchemy import create_engine

from midas.conf.config import OPERATIONAL_DB

engine = create_engine(OPERATIONAL_DB, echo=True)
