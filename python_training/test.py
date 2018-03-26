import pytest
from python_training.member import Member
from python_training.utils import get_engine_and_session


@pytest.fixture()
def test_session(scope='session'):
    test_session = get_engine_and_session()[1]
    return test_session


def test_first_user_exist():
    assert test_session.query(Member).first()