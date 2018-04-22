
from midas.core.event_member_enrollment import event_enrollment_association_table
from midas.core.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from midas.core.basic_table import BasicTable


class Event(Base, BasicTable):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    location = Column(String(256))

    members = relationship('Member', secondary=event_enrollment_association_table,
                           back_populates='events')

    def __repr__(self):
        return f'<Object:{type(self).__name__} Date: {self.date}, Location: {self.location}>'


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
