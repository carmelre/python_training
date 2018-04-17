from python_training.member import add_member
from python_training.event import add_event
from python_training.organization import add_organization
from python_training.config import MEMBERS_INFO, EVENTS_INFO, ORGANIZATIONS_INFO
from python_training.base import Base
from python_training.engine import engine
from python_training.utils import get_session


def insert_info(engine, session):
    """
    Adds some sample rows to the DB.

    :param engine: The engine we use to communicate with the db.
    :param session: The session we use to communicate with the db.
    """
    Base.metadata.create_all(engine)
    members = [add_member(session, **kwargs) for kwargs in MEMBERS_INFO]
    events = [add_event(session, **kwargs) for kwargs in EVENTS_INFO]
    organizations = [add_organization(session, **kwargs) for kwargs in ORGANIZATIONS_INFO]
    organizations[0].members.extend(members[:2])
    events[0].members.extend(members)
    events[1].members.extend(members)
    session.commit()


def main():
    session = get_session(engine)
    insert_info(engine, session)


if __name__ == '__main__':
    main()
