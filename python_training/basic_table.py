
class QueryModifier:
    """
    An object that holds and allows modification of an SQLAlchemy query.
    """

    def __init__(self, session, table_object, query=None):
        """
        Instantiates the object with a basic return all query.

        :param session: A session to be used.
        :param table_object: The table that the query will be executed upon.
        :param query: The previous query (if there is so).
        """
        self.table_object = table_object
        self.session = session
        if query is not None:
            self.query = query
        else:
            self.query = self.session.query(table_object)

    def __getattr__(self, item):
        return getattr(self.query, item)

    def refine(self, *args, **kwargs):
        """
        Adds a new condition to the query, and returns a new QueryModifier instance.
        A new object is returned so queries can branch:
        q1 = Table.get()
        q2 = q1.refine(condition1)
        q3 = q1.refine(condition2)

        :param condition: An SQLalchemy condition that would be applied to the query.
        :return: A new instance of QueryModifier.
        """
        new_query = self.query

        for arg in args:
            new_query = new_query.filter(arg)
        for key, value in kwargs.items():
            new_query = new_query.filter(getattr(self.table_object, key) == value)

        return QueryModifier(session=self.session, query=new_query, table_object=self.table_object)

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
    def get(cls, session) -> QueryModifier:
        """
        Creates a QueryModifier that holds a plain query upon the table (seletc *).
        :return: A new QueryModifier instance.
        """
        return QueryModifier(table_object=cls, session=session)
