from midas.core.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from midas.core.basic_table import BasicTable


class Organization(Base, BasicTable):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    prime_location = Column(String(256))

    members = relationship('Member', back_populates='organization')

    def __repr__(self):
        return f'Object:{type(self).__name__} Name: {self.name}, Prime Location: {self.prime_location}'


def add_organization(session, name, prime_location) -> Organization:
    """
    Creates a new Organization and adds it to the DB.

    :param session: The session that would bw used to establish a connection to the db.
    :param name: The name of the Organization.
    :param prime_location: The primary location of the Organization.
    :return The new organization object that has been created.
    """
    new_organization = Organization(name=name, prime_location=prime_location)
    session.add(new_organization)
    session.commit()
    return new_organization
