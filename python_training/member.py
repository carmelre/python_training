from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from python_training.base import Base
from python_training.organization import Organization

class Member(Base):

    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    role = Column(String(256))
    location = Column(String(256))
    organization_id = Column(Integer, ForeignKey(Organization.id))

    organization = relationship(Organization)

    def __repr__(self):
        return f'First Name: {self.first_name}, Last Name: {self.last_name},' \
               f' Role: {self.role}, Location: {self.location}'


def add_member(session, first_name, last_name, role, location):
    """
    Creates a new Member and adds it to the DB.

    :param session: The session that would bw used to establish a connection to the db.
    :param first_name: The first name of the Member.
    :param last_name: The last name of the Member.
    :param role: The role of the Member.
    :param location: The location of the Member.
    """
    new_member = Member(first_name=first_name, last_name=last_name, role=role, location=location)
    session.add(new_member)
    session.commit()
    return new_member
