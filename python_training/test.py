import pytest
from datetime import datetime
from python_training.member import add_member, Member
from python_training.event import add_event, Event
from python_training.organization import add_organization, Organization
from python_training.utils import get_engine_and_session
from python_training.config import TEST_DB
from python_training.utils import create_tables

create_tables(db_path=TEST_DB)

members_info = [{'first_name': 'carmel', 'last_name': 'reubinoff', 'role': 'dev', 'location': 'Tozeret Haaretz'},
                {'first_name': 'Anya', 'last_name': 'tch', 'role': 'dev', 'location': 'Tozeret Haaretz'},
                {'first_name': 'Alon', 'last_name': 'Shenkler', 'role': 'dev', 'location': 'Tozeret Haaretz'}]
organizations_info = [{'name': 'Sygnia', 'prime_location': 'Tozeret Haaretz'},
                      {'name': 'Claroty', 'prime_location': 'Tozeret Haaretz'}]
events_info = [{'date': datetime.now(), 'location': 'Mizpe Hayamim'},
               {'date': datetime.now(), 'location': 'Zappa Herzliya'}]


@pytest.fixture()
def member1():
    return Member(**members_info[0])


@pytest.fixture()
def member2():
    return Member(**members_info[1])


@pytest.fixture()
def member3():
    return Member(**members_info[2])


@pytest.fixture()
def event1():
    return Event(**events_info[0])


@pytest.fixture()
def event2():
    return Event(**events_info[1])


@pytest.fixture()
def organization1():
    return Organization(**organizations_info[0])


@pytest.fixture()
def session():
    test_session = get_engine_and_session(TEST_DB)[1]
    yield test_session
    test_session.rollback()
    test_session.commit()


@pytest.mark.parametrize('add_func, kwargs',
                         [(add_member, members_info[0]),
                          (add_organization, organizations_info[0]),
                          (add_event, events_info[0])])
def test_add_objects(add_func, kwargs, session):
    new_object = add_func(session, **kwargs)
    object_type = type(new_object)
    assert session.query(object_type).filter(object_type.id == new_object.id)


def test_add_members_to_organization_via_organization(session, member1, member2, organization1):
    organization1.members.extend([member1, member2])
    session.add(organization1)
    session.commit()
    retrieved_organization = session.query(Organization).filter(Organization.id == organization1.id).one()
    assert retrieved_organization.members == [member1, member2]


def test_add_members_to_organization_via_member(session, member1, organization1):
    member1.organization = organization1
    session.add(member1)
    session.commit()
    retrieved_member = session.query(Member).filter(Member.id == member1.id).one()
    assert retrieved_member.organization == organization1


def test_add_members_to_events(session, member1, member2, member3, event1, event2):
    event1.members.extend([member1, member2])
    event2.members.extend([member2, member3])
    session.add(event1, event2)
    session.commit()
    assert {event1, event2}.issubset(set(member2.events))
    assert set(event1.members).issubset({member1, member2})