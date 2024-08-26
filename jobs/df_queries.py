from typing import Any
from libs.db import execute_sql
from collections import defaultdict
"""
Queries the db for relevant info needed in st charts/visuals
"""

def find_histogram_info() -> dict[str, Any]:
    """
    Finds all repeating entities and matches them to their frequency
    """
    entitiesInfo = defaultdict(list)
    sql = """
    SELECT entity
    FROM entities_to_articles
    GROUP BY entity
    HAVING COUNT(entity) > 1;
    """
    repeated_entities = execute_sql(sql=sql, return_response=True)

    if repeated_entities:
        for entity in repeated_entities:
            entity = entity[0]
            params = {'entity': entity}

            sql = f"""
            SELECT author
            FROM entities_to_articles
            WHERE LOWER(entity) LIKE '%' || LOWER(:entity) || '%';
            """
            authors = execute_sql(sql=sql, params=params, return_response=True)
            # stripping tuples
            if authors: authors = [author[0] for author in authors]
            # adding to dictionary of repeated entities
            entitiesInfo['Entities'].append(entity)
            entitiesInfo['Count'].append(len(authors) if authors else 0)
            entitiesInfo['Authors'].append(authors)

    return entitiesInfo

def find_table_info() -> dict[str, Any]:
    """
    Collects all database article info ...
    """



    return