import pytest
from python_training.member import Member, add_member
from python_training.event import Event, add_event
from python_training.organization import Organization, add_organization
from python_training.utils import get_engine_and_session
from python_training.config import TEST_DB
from python_training.utils import create_tables


create_tables(db_path=TEST_DB)


@pytest.fixture(autouse=True)
def session():
    test_session = get_engine_and_session(TEST_DB)[1]
    yield test_session
    test_session.rollback()
    test_session.commit()

@pytest.mark.parametrize()
def test_add_user(session):
    new_member = add_member(session, 'carmel', 'reubinoff', 'dev', 'Sygnia')
    assert session.query(Member).filter(Member.id == new_member.id)


def test_add_event(session):


def make_sure_session_was_cleaned(session):
    assert session.query(Member).all == []