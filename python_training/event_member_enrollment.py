from sqlalchemy import Table, Column, Integer, ForeignKey
from python_training.base import Base

event_enrollment_association_table = Table('event_member_association', Base.metadata,
                                           Column('event_id', Integer,
                                                  ForeignKey('events.id'), primary_key=True),
                                           Column('member_id', Integer,
                                                  ForeignKey('members.id'), primary_key=True))
