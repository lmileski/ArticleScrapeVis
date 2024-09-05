from sqlalchemy import create_engine, Table, MetaData, literal_column, delete, text
from sqlalchemy.dialects.postgresql import insert
import os 


ALCHEMY_DATABASE_URL = os.getenv('ALCHEMY_DATABASE_URL')
engine = create_engine(ALCHEMY_DATABASE_URL)
con = engine.connect()


def add_articles(article_records: list[dict]):
    article_table = Table("article", MetaData(schema="public"), autoload_with=engine)
    upsert_query = insert(article_table)
    upsert_query = upsert_query.on_conflict_do_update(
        index_elements=['url'],
        set_= {
            article_table.c.title: upsert_query.excluded.title
        }
    )
    upsert_query = upsert_query.returning(literal_column("url"), literal_column("id"))
    response = con.execute(upsert_query.values(article_records)).mappings().all()
    return response 


def reset_entities(article_ids: list):
    entity_table = Table("article_entities", MetaData(schema="public"), autoload_with=engine)
    delete_query = delete(entity_table).where(entity_table.c.article_id.in_(article_ids))
    con.execute(delete_query)


def add_entities(entity_records: list[dict]):
    entity_table = Table("article_entities", MetaData(schema="public"), autoload_with=engine)
    insert_query = insert(entity_table)
    insert_query = insert_query.on_conflict_do_nothing(
        index_elements=['article_id','entity']
    )
    con.execute(insert_query.values(entity_records))


def execute_sql(sql: str, return_response: bool = False, commit: bool = False, close_connection: bool = False):
    sql_query = text(sql)
    try:
        response = con.execute(sql_query)
        response_body = response.mappings().all() if return_response else None 

        if commit:
            con.commit()
        if close_connection:
            con.close()
        return response_body  

    except Exception as e:
        con.rollback()
        con.close()
        print("Rolling back transaction due to error.")
        raise e
    

def clear_tables():
    entity_table = Table("article_entities", MetaData(schema="public"), autoload_with=engine)
    article_table = Table("article", MetaData(schema="public"), autoload_with=engine)
    
    con.execute(delete(entity_table))
    con.execute(delete(article_table))