"""
Queries the db for relevant info needed in st charts/visuals
"""
from typing import Any
from libs.db import execute_sql

def find_top_headline_info() -> dict[str, Any]:
    """
    Finds all repeating entities and matches them to their
    - frequency
    - article headlines:
        - author
        - date
        - url
    Returns a dictionary of all this data
    """

    entitiesInfo = {}
    sql = """
    SELECT entity
    FROM entities_to_articles
    WHERE LOWER(author) NOT LIKE '%' || LOWER(entity) || '%'
    GROUP BY entity
    HAVING COUNT(entity) > 1;
    """
    repeated_entities = execute_sql(sql=sql, return_response=True)

    if repeated_entities:
        for entity in repeated_entities:
            entity = entity[0]
            params = {'entity': entity}

            sql = f"""
            SELECT title, url, date, author
            FROM entities_to_articles
            WHERE LOWER(entity) LIKE '%' || LOWER(:entity) || '%';
            """
            entity_info = execute_sql(sql=sql, params=params, return_response=True)

            # adding to dictionary of repeated entities
            entitiesInfo[entity] = entity_info

    return entitiesInfo

def find_all_article_info() -> list[tuple]:
    """
    Collects all articles and sorts them by their
    - title (w/URL)
    - author
    - date
    - all entities
    """

    sql = """
    SELECT * FROM article
    ORDER BY date DESC; 
    """
    articles_w_entities = []
    all_articles = execute_sql(sql=sql, return_response=True)

    if all_articles:
        for i, article in enumerate(all_articles):
            id = article[0]
            sql = """
            SELECT entity FROM entities_to_articles
            WHERE article_id = :id;
            """
            params = {'id': id}
            entities = execute_sql(sql=sql, params=params, return_response=True)
            entity_article = list(article)
            # stripping entities of () and converting to a single str
            if entities: entity_article.append(", ".join([entity[0] for entity in entities]))
            articles_w_entities.append(tuple(entity_article))

    return articles_w_entities or []