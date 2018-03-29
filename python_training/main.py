from python_training.member import add_member
from python_training.event import add_event, Event
from python_training.organization import add_organization
from python_training.config import MEMBERS_INFO, EVENTS_INFO, ORGANIZATIONS_INFO


def insert_info(session):
    """
    Adds inserts to the DB.

    :param session: The session we use to communicate with the db.
    """
    members = [add_member(session, **kwargs) for kwargs in MEMBERS_INFO]
    events = [add_event(session, **kwargs) for kwargs in EVENTS_INFO]
    organizations = [add_organization(session, **kwargs) for kwargs in ORGANIZATIONS_INFO]
    organizations[0].members.extend(members[:2])
    events[0].members.extend(members[1:])
    events[1].members.append(members[0])
    session.commit()


def main():
    print(Event.get().refine('events.id' == 1).run())


if __name__ == '__main__':
    main()
