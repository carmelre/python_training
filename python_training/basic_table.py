from python_training.utils import get_connection
from python_training.config import OPERATIONAL_DB


class QueryModifier:
    """
    An object that holds and allows modification of an SQLAlchemy query.
    """

    def __init__(self, session=None, table_object=None, query=None):
        """
        Instantiates the object with a basic return all query.

        :param session: A session to be used. If no session is provided a new one is opened.
        :param table_object: The table that the query will be executed upon.
        :param query: The previous query (if there is so).
        """
        if session is None:
            self.session = get_connection(OPERATIONAL_DB, get_session=True)
        else:
            self.session = session
        if query is not None:
            self.query = query
        elif table_object is not None:
            self.query = self.session.query(table_object)
        else:
            raise ValueError('No table has been provided')

    def __getattr__(self, item):
        return getattr(self.query, item)

    def refine(self, condition):
        """
        Adds a new condition to the query, and returns a new QueryModifier instance.
        A new object is returned so queries can branch:
        q1 = Table.get()
        q2 = q1.refine(condition1)
        q3 = q1.refine(condition2)

        :param condition: An SQLalchemy condition that would be applied to the query.
        :return: A new instance of QueryModifier.
        """
        return QueryModifier(session=self.session, query=self.query.filter(condition))

    def run(self):
        """
        Executes the query and returns the result.

        :return: The result of the query.
        """
        return self.query.all()

    def __len__(self):
        return self.query.count()


class BasicTable:
    @classmethod
    def get(cls) -> QueryModifier:
        """
        Creates a QueryModifier that holds a plain query upon the table (seletc *).
        :return: A new QueryModifier instance.
        """
        return QueryModifier(table_object=cls)
