from python_training.member import add_member, Member
from python_training.event import add_event, Event
from python_training.organization import add_organization
from python_training.config import MEMBERS_INFO, EVENTS_INFO, ORGANIZATIONS_INFO
from python_training.utils import get_connection, create_tables
from python_training.config import OPERATIONAL_DB


def insert_info(engine, session):
    """
    Adds some sample rows to the DB.

    :param session: The session we use to communicate with the db.
    """
    create_tables(engine)
    members = [add_member(session, **kwargs) for kwargs in MEMBERS_INFO]
    events = [add_event(session, **kwargs) for kwargs in EVENTS_INFO]
    organizations = [add_organization(session, **kwargs) for kwargs in ORGANIZATIONS_INFO]
    organizations[0].members.extend(members[:2])
    events[0].members.extend(members[1:])
    events[1].members.append(members[0])
    session.commit()


def main():
    session, engine = get_connection(OPERATIONAL_DB, get_session=True, get_engine=True)
    insert_info(engine, session)
    print(Member.get().refine(Event.id == 1))
    print(Event.get().refine(Event.id == 1).run())


if __name__ == '__main__':
    main()
