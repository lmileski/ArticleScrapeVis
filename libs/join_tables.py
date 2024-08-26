from libs.db import execute_sql

def create_joint_table():
    """
    Creates a joint table in the DB based off
    entities' matching article_id foreign key
    """

    sql = """
    CREATE TABLE IF NOT EXISTS public.entities_to_articles AS
    SELECT
        ae.entity,
        a.id AS article_id,
        a.author,
        a.title,
        a.date,
        a.url
    FROM
        public.article a
    LEFT JOIN
        public.article_entities ae
    ON
        a.id = ae.article_id;
    """

    execute_sql(sql=sql, commit=True)