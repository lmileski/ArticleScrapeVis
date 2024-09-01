"""
Run this file once after provisioning a postgres DB to create the needed tables for the app to work properly.
"""
from libs import db 

def create_tables():
    sql = """
    CREATE SCHEMA IF NOT EXISTS public;

    CREATE TABLE IF NOT EXISTS public.article (
        id SERIAL PRIMARY KEY,
        author TEXT NOT NULL,
        title TEXT NOT NULL,
        date TIMESTAMPTZ NULL,
        url TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS public.article_entities (
        id SERIAL PRIMARY KEY,
        article_id INT NOT NULL,
        entity TEXT,
        FOREIGN KEY (article_id) REFERENCES public.article(id),
        UNIQUE(article_id, entity)
    );

    CREATE VIEW public.v_articles_w_entities AS 
    SELECT
        a.id AS article_id,
        a.author,
        a.title,
        a.date,
        a.url,
        ae.entity
    FROM
        public.article a
    LEFT JOIN
        public.article_entities ae
    ON
        a.id = ae.article_id; 
    """

    sql = db.text(sql)
    con = db.engine.connect()
    con.execute(sql)
    con.commit()
    con.close()


def clear_tables():
    sql = """
    DELETE FROM public.article_entities;
    DELETE FROM public.article;
    """
    sql = db.text(sql)
    con = db.engine.connect()
    con.execute(sql)
    con.commit()
    con.close()


def drop_tables():
    sql="""
    DROP TABLE IF EXISTS public.article_entities;
    DROP TABLE IF EXISTS public.article;
    DROP VIEW IF EXISTS public.v_articles_w_entities;
    """
    sql = db.text(sql)
    con = db.engine.connect()
    con.execute(sql)
    con.commit()
    con.close()