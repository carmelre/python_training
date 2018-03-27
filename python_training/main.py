from python_training.utils import get_engine_and_session, create_tables
from python_training.member import add_member
from python_training.event import add_event
from python_training.organization import add_organization
import datetime


def main():
    engine, session = get_engine_and_session()
    create_tables(engine)
    member = add_member(session, 'anya', 'tch', 'dev', 'sygnia')
    event = add_event(session, datetime.datetime.now(), 'Jerusalem')
    organization = add_organization(session, 'Team8', 'Tel Aviv')
    member.organization = organization
    event.members.append(member)
    print(event.members)
    print(member.events)

if __name__ == '__main__':
    main()
