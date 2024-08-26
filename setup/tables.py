"""
Run this file once after provisioning a postgres DB to create the needed tables for the app to work properly.
"""
from libs.db import execute_sql

def create_tables(sql=""):
    sql += """
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
        FOREIGN KEY (article_id) REFERENCES public.article(id)
    );
    """

    execute_sql(sql=sql, commit=True)