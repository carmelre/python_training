from midas.core.event import Event
from midas.core.member import Member
from midas.core.basic_table import QueryModifier
from sqlalchemy import func
from sqlalchemy.orm import aliased

from midas.core.organization import Organization


def members_that_are_not_at_organization_location(session) -> QueryModifier:
    """
    Creates a query that returns members that are not stationed at their organizations location.

    :param session: The session that will be used to communicate with the database.
    :return: A QueryModifier object that holds the new query.
    """
    return QueryModifier(session,
                         table_object=Member,
                         query=session.query(Member).join(Organization).
                         filter(Member.location != Organization.prime_location))


def last_event_per_member(session) -> QueryModifier:
    """
    Creates a query that returns the last event each member took part in.

    :param session: The session that will be used to communicate with the database.
    :return: A QueryModifier object that holds the new query.
    """
    return QueryModifier(session,
                         table_object=Member,
                         query=session.query(Member, func.max(Event.date)).join(Event, Member.events).
                         group_by(Member.id))


def number_of_members_in_organization(session) -> QueryModifier:
    """
    Creates a query that counts the number of members in each organization.

    :param session: The session that will be used to communicate with the database.
    :return: A QueryModifier object that holds the new query.
    """
    return QueryModifier(session,
                         table_object=Organization,
                         query=session.query(Organization, func.count(Member.id))
                         .outerjoin(Member, Organization.members).group_by(Organization.id))


def number_of_organizations_each_event(session) -> QueryModifier:
    """
    Creates a query that counts the number of organizations that took part in each event.

    :param session: The session that will be used to communicate with the database.
    :return: A QueryModifier object that holds the new query.
    """
    return QueryModifier(session, table_object=Event,
                         query=session.query(Event, func.count(Organization.id))
                         .join(Member, Event.members)
                         .join(Organization, Member.organization))


def people_you_may_know(session):
    """
    Creates a query that finds for each member other members he may know
    (if they have attended the same event).

    :param session: The session that will be used to communicate with the database.
    :return: The result of the query.
    """
    member_table1 = aliased(Member)
    member_table2 = aliased(Member)
    raw_results = session.query(member_table1, member_table2) \
        .join(Event, member_table1.events).join(member_table2, Event.members) \
        .filter(member_table1.id != member_table2.id).all()
    members_to_friends = {}
    for result in raw_results:
        if result[0] in members_to_friends:
            members_to_friends[result[0]].add(result[1])
        else:
            members_to_friends[result[0]] = {result[1]}
    return members_to_friends
