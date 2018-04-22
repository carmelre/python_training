import pytest
from sqlalchemy import create_engine

from midas.conf.mock_data import MEMBERS_INFO, ORGANIZATIONS_INFO, EVENTS_INFO
from midas.core.base import Base
from midas.core.event import add_event, Event
from midas.core.member import add_member, Member
from midas.core.organization import add_organization, Organization
from midas.queries.queries import members_that_are_not_at_organization_location, last_event_per_member, \
    number_of_organizations_each_event, number_of_members_in_organization, people_you_may_know
from midas.utils.utils import get_session

TEST_DB_FILE_NAME = 'midas_test.db'


@pytest.fixture()
def test_db(tmpdir):
    db_file_path = tmpdir.mkdir('db_dir').join(TEST_DB_FILE_NAME)
    db_url = f'sqlite:///{str(db_file_path)}'
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(test_db):
    with get_session(test_db) as test_session:
        return test_session


@pytest.fixture()
def member1():
    return Member(**MEMBERS_INFO[0])


@pytest.fixture()
def member2():
    return Member(**MEMBERS_INFO[1])


@pytest.fixture()
def member3():
    return Member(**MEMBERS_INFO[2])


@pytest.fixture()
def event1():
    return Event(**EVENTS_INFO[0])


@pytest.fixture()
def event2():
    return Event(**EVENTS_INFO[1])


@pytest.fixture()
def organization1():
    return Organization(**ORGANIZATIONS_INFO[0])

@pytest.fixture()
def organization2():
    return Organization(**ORGANIZATIONS_INFO[1])


@pytest.mark.parametrize('add_func, kwargs',
                         [(add_member, MEMBERS_INFO[0]),
                          (add_organization, ORGANIZATIONS_INFO[0]),
                          (add_event, EVENTS_INFO[0])])
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


@pytest.mark.parametrize('table_object, instance',
                         [(Member, member1()),
                          (Event, event1()),
                          (Organization, organization1())])
def test_refine_func(table_object, instance, session):
    session.add(instance)
    regular_query = session.query(table_object).filter(table_object.id == 1).all()
    get_query = table_object.get(session).refine(table_object.id == 1).all()
    assert len(get_query) == len(regular_query) == 1
    assert get_query[0].id == regular_query[0].id
    assert isinstance((get_query[0]), table_object) and isinstance((regular_query[0]), table_object)


def test_query_members_not_in_organization_location(session, member2, organization1):
    member2.organization = organization1
    session.add(member2)
    session.commit()
    assert member2.id in [member.id for member in members_that_are_not_at_organization_location(session).all()]


def test_query_last_event_per_member(session, member3, event1):
    member3.events.append(event1)
    session.add(member3)
    session.commit()
    query_result = last_event_per_member(session).all()
    assert any([result for result in query_result if result[0] == member3 and result[1] == event1.date])


def test_query_number_of_members_in_organization(session, member1, member2, organization1):
    organization1.members.extend([member1, member2])
    session.add(organization1)
    session.commit()
    assert number_of_members_in_organization(session).all()[0][1] == 2


def test_number_of_organizations_each_event(session, member1, member2, organization1, organization2, event1):
    member1.organization = organization1
    member2.organization = organization2
    event1.members.extend([member1, member2])
    session.add(event1)
    session.commit()
    assert number_of_organizations_each_event(session).all()[0][1] == 2


def test_people_you_may_know(session, member1, member2, event1):
    event1.members.extend([member1, member2])
    session.add(event1)
    session.commit()
    result = people_you_may_know(session)
    assert member2 in result[member1]
    assert len(result[member1]) == 1
