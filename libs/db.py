def execute_sql(sql: str, return_response: bool = False, commit: bool = False ) -> any:
    """
    executes SQL statement against db.
    :param sql - a valid pgSQL statement.
    :param return_response - if `True`, returns any response the query generates (ie, select)
    :param commit - if `True`, commits a statement against the db.
    :returns None or an iterable.
    """
    pass


