"""
Gets a collection of headlines and generates extracted entities for them,
then uploads both objects to db.
"""
from libs.headlines import get_headlines
from libs.dandelion import extract_entities
from libs.db import execute_sql

# includes author/title/date/URL
top_headlines: list[dict] = get_headlines()

# extracing entities w/ dandelion then adding to SQL script
for article in top_headlines:

    # adding article info
    sql = (
    """
    INSERT INTO dbo.article (article_author, article_title, article_date, article_url)
    VALUES (%s, %s, %s, %s)
    RETURNING id
    """,
    (article['author'], article['title'], article['date'], article['url'])
    )

    # grabbing this article's id by uploading to db
    last_id = execute_sql(sql=sql, return_response=True, commit=False) # type: ignore

    # find and adding dandelion entity info
    entities = extract_entities(article['title'])

    for entity in entities:
        sql = (
        """
        INSERT INTO dbo.article_entities (article_id, entity, confidence)
        VALUES (%s, %s, %s)
        """,
        (last_id, entity['label'], entity['confidence']) # type: ignore
        )
        # uploading to db
        execute_sql(sql=sql, commit=False) # type: ignore