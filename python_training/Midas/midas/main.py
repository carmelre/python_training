from midas.conf.mock_data import MEMBERS_INFO, EVENTS_INFO, ORGANIZATIONS_INFO
from midas.core.base import Base
from midas.core.engine import engine
from midas.core.event import add_event
from midas.core.member import add_member, Member
from midas.core.organization import add_organization
from midas.utils.utils import get_session


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
    with get_session(engine) as session:
        # insert_info(engine, session)
        r = Member.get(session).refine(Member.id > 1, id=4).order_by(Member.id).run()
        print(r)


if __name__ == '__main__':
    main()
