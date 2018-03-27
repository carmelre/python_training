from python_training.member import add_member
from python_training.event import add_event
from python_training.organization import add_organization
from python_training.config import OPERATIONAL_DB, MEMBERS_INFO, EVENTS_INFO, ORGANIZATIONS_INFO
from python_training.utils import create_tables, get_engine_and_session


def insert_info(session):
    members = [add_member(session, **kwargs) for kwargs in MEMBERS_INFO]
    events = [add_event(session, **kwargs) for kwargs in EVENTS_INFO]
    organizations = [add_organization(session, **kwargs) for kwargs in ORGANIZATIONS_INFO]
    organizations[0].members.extend(members[:2])
    organizations[1].members.append(members[2])
    events[0].members.extend(members[1:])
    events[1].members.append(members[0])
    session.commit()


def main():
    engine, session = get_engine_and_session(OPERATIONAL_DB)
    create_tables(engine)
    insert_info(session)


if __name__ == '__main__':
    main()

