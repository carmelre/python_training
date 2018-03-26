from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from .config import DB_PATH

Base = declarative_base()


class Member(Base):

    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    role = Column(String(256))
    location = Column(String(256))

    def __repr__(self):
        return f'First Name: {self.first_name}, Last Name: {self.last_name},' \
               f' Role: {self.role}, Location: {self.location}'


def main():

    engine = create_engine(DB_PATH, echo=True)
    # carmel = Member(first_name='Carmel', last_name='Reubinoff', role='dev', location='Team8')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    # session.add(carmel)
    # session.commit()
    print(session.query(Member).all)


if __name__ == '__main__':
    main()
