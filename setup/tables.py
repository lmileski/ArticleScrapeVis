"""
Run this file once after provisioning a postgres DB to create the needed tables for the app to work properly.
"""
import sys
sys.path.append('../ArticleScrapeVis')
from libs.db import execute_sql


sql = """
CREATE SCHEMA IF NOT EXISTS dbo;
CREATE TABLE IF NOT EXISTS dbo.article (
    id SERIAL,
    article_author TEXT NOT NULL,
    article_title TEXT NOT NULL,
    article_date TIMESTAMPTZ NULL,
    article_url TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dbo.article_entities (
    id SERIAL,
    article_id INT NOT NULL,
    entity TEXT,
    confidence FLOAT NOT NULL
);
"""

execute_sql(sql=sql, return_response=False, commit=True) # type: ignore