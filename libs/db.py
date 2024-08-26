from typing import Optional
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def execute_sql(table_name: Optional[str] = None, sql: Optional[str] = None, df: Optional[pd.DataFrame] = None,
                params: Optional[dict] = None, return_response: bool = False, commit: bool = False) -> Optional[list[tuple]]:
    """
    executes SQL statement against db.
    :param sql - sql text to be executed
    :param df - pandas df to be converted into sql then executed
    :param return_response - if `True`, returns any response the query generates (ie, select)
    :param commit - if `True`, commits a statement against the db.
    :returns None or an iterable.
    """
    
    # connecting to db
    engine = create_engine('postgresql+psycopg2://postgres:biscuits@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()

    response = None
    # beginning transaction
    try:
        if sql:
            result = session.execute(text(sql), params)
            if return_response:
                response = result.fetchall()
        if isinstance(df, pd.DataFrame) and table_name:
            # converting df to sql and executing
            df.to_sql(table_name, engine, if_exists='append', index=False)
        # committing only if desired
        if commit:
            session.commit()
            # transaction successful
    
    except Exception as e:
        # rolling back transaction in case of error
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")

    finally:
        session.close()
    
    return response # type: ignore