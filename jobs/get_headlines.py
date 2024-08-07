"""
Gets a collection of headlines and generates extracted entities for them,
then uploads both objects to db.
"""

from libs.headlines import get_headlines
from libs.dandelion import extract_entities
from libs.db import execute_sql

sql = []
# includes author/title/date/URL
top_headlines: list[dict] = get_headlines()
# extracing entities w/ dandelion then adding to SQL script
for article in top_headlines:
    entities = extract_entities(article['text'])

    sql.append((
    """
    INSERT INTO dbo.article (article_author, article_title, article_date, article_url)
    VALUES (%s, %s, %s, %s)
    """,
    (article['author'], article['title'], article['date'], article['url'])
    ))

print(sql)

# uploading to db
execute_sql(sql=sql, commit=False) # change to True if actually running app