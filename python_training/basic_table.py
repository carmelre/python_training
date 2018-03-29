from python_training.utils import get_engine_and_session
from python_training.config import OPERATIONAL_DB


class BasicTable:
    @classmethod
    def get(cls) -> QueryModifier:
        """
        Creates a QueryModifier that holds a plain query upon the table (seletc *).
        :return: A new QueryModifier instance.
        """
        return QueryModifier(cls)


class QueryModifier:
    """
    An object that holds and allows modification of an SQLAlchemy query.
    """

    def __init__(self, table_object):
        """
        Instantiates the object with a basic query upon the database.

        :param table_object: The table that the query will be executed upon.
        """
        session = get_engine_and_session(OPERATIONAL_DB)[1]
        self.query = session.query(table_object)

    def refine(self, condition):
        """
        Adds a new condition to the query, and returns a new QueryModifier instance.
        This way we can support this use case:
        q1 = Table.get()
        q2 = q1.refine(condition1)
        q3 = q1.refine(condition2)

        :param condition: An SQLalchemy condition that would be applied to the query.
        :return: A new instance of QueryModifier.
        """
        return QueryModifier(self.query.filter(condition))

    def run(self):
        """
        Executes the query and returns the result.

        :return: The result of the query.
        """
        return self.query.all()

    def __len__(self):
        return self.query.count()
