from typing import Optional
import psycopg2

def execute_sql(sql: tuple | str, return_response: bool = False, commit: bool = False) -> Optional[list[tuple]]:
    """
    executes SQL statement against db.
    :param sql - a valid pgSQL statement.
    :param return_response - if `True`, returns any response the query generates (ie, select)
    :param commit - if `True`, commits a statement against the db.
    :returns None or an iterable.
    """
    # connecting to db
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres',
                            password='biscuits', port=5432)
    cur = conn.cursor()

    # sql can either be plain strs or embedded w/ tuples
    if isinstance(sql, str):
        cur.execute(sql)
    else:
        cur.execute(sql[0], sql[1])

    response = None
    if return_response:
        response = cur.fetchall()
    if commit:
        conn.commit()
    
    cur.close()
    conn.close()

    return response