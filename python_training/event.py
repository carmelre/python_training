from sqlalchemy import Column, Integer, String, DateTime
from python_training.base import Base


class Event(Base):

    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    location = Column(String(256))

    def __repr__(self):
        return f'Date: {self.date}, Location: {self.location}'


def add_event(session, date, location):
    """
    Creates a new Event and adds it to the DB.

    :param session: The session that would bw used to establish a connection to the db.
    :param date: The date in which the Event has occurred (DateTime)
    :param location: The location in which the Event has occurred.
    :return: The new Event that has been created.
    """
    new_event = Event(date=date, location=location)
    session.add(new_event)
    session.commit()
    return new_event
