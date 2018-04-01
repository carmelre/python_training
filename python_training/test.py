import pytest
from python_training.member import add_member, Member
from python_training.event import add_event, Event
from python_training.organization import add_organization, Organization
from python_training.utils import get_engine_and_session
from python_training.config import TEST_DB, MEMBERS_INFO, ORGANIZATIONS_INFO, EVENTS_INFO
from python_training.utils import create_tables

create_tables(db_path=TEST_DB)


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
def session():
    test_session = get_engine_and_session(TEST_DB)[1]
    yield test_session
    test_session.rollback()
    test_session.commit()


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


# @pytest.mark.parametrize('table_object, instance',
#                          [(Member, member1),
#                           (Event, event1),
#                           (Organization, organization1)])
# def test_refine_func(table_object, instance, session):
#     assert table_object.get().refine(table_object.id == instance.id).run() == session.query(table_object).filter(table_object.id == instance.id)

def test_refine_func(session, member1):
     assert Member.get().refine(Member.id == member1.id).run() == session.query(Member).filter(Member.id == member1.id)