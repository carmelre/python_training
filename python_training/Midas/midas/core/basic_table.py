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
        self.query = query if query is not None else self.session.query(table_object)

    def __getattr__(self, item):
        self.query = getattr(self.query, item)
        return self

    def __call__(self, *args):
        new_query = self.query(*args)
        return QueryModifier(session=self.session, query=new_query, table_object=self.table_object)

    def refine(self, *args, **kwargs):
        """
        Adds a new condition to the query, and returns a new QueryModifier instance.
        A new object is returned so queries can branch:
        q1 = Table.get()
        q2 = q1.refine(condition1)
        q3 = q1.refine(condition2)

        :param args: An SQLalchemy condition (or a list of comditions) that would be applied to the query.
        :param kwargs: Keyword conditions that would be added to the query as filters.
        :return: A new instance of QueryModifier.
        """
        new_query = self.query

        for arg in args:
            new_query = new_query.filter(arg)
        for key, value in kwargs.items():
            new_query = new_query.filter(getattr(self.table_object, key) == value)

        return QueryModifier(session=self.session, query=new_query, table_object=self.table_object)

    def all(self):
        """
        Executes the query and returns all the results.

        :return: The result of the query.
        """
        return self.query.all()

    def one(self):
        """
        Executes the query and returns one result.

        :return: The result of the query.
        """
        return self.query.one()

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
