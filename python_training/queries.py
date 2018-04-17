from python_training.member import Member
from python_training.event import Event
from python_training.organization import Organization
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased


def members_that_are_not_at_organization_location(session):
    """
    Creates a query that returns members that are not stationed at their organizations location.

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    return session.query(Member).join(Organization). \
        filter(Member.location != Organization.prime_location).all()


def last_event_per_member(session):
    """
    Creates a query that returns the last event each member took part in.

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    return session.query(Member, func.max(Event.date)).join(Event, Member.events).group_by(Member.id).all()


def number_of_members_in_organization(session):
    """
    Creates a query that counts the number of members in each organization.

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    return session.query(Organization, func.count(Member.id)).outerjoin(Member, Organization.members) \
        .group_by(Organization.id).all()


def number_of_organizations_each_event(session):
    """
    Creates a query that counts the number of organizations that took part in each event.

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    return session.query(Event, func.count(Organization.id)) \
        .join(Member, Event.members) \
        .join(Organization, Member.organization).all()


def people_you_may_know(session):
    """
    Creates a query that finds for each member other members he may know
    (if they have attended the same event).

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    member_table1 = aliased(Member)
    member_table2 = aliased(Member)
    raw_results = session.query(member_table1, member_table2)\
        .join(Event, member_table1.events).join(member_table2, Event.members)\
        .filter(member_table1.id != member_table2.id).all()
    members_to_friends = {}
    for result in raw_results:
        if result[0] in members_to_friends:
            members_to_friends[result[0]].append(result[1])
        else:
            members_to_friends[result[0]] = {result[1]}
    return members_to_friends


