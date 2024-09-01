"""
Queries the db for relevant info needed in st charts/visuals
"""
from typing import Any
from libs.db import execute_sql
import pandas as pd 

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
    WITH repeat_entities AS (
        SELECT entity
        FROM public.v_articles_w_entities
        WHERE LOWER(author) NOT LIKE '%' || LOWER(entity) || '%'
        GROUP BY entity
        HAVING COUNT(entity) > 1
    )

    SELECT 
        re.entity, 
        article.title, 
        article.url, 
        article.date, 
        article.author 
    FROM public.article_entities e
    INNER JOIN repeat_entities re on re.entity = e.entity  
    INNER JOIN public.article article on article.id = e.article_id
    """
    repeated_entities = execute_sql(sql=sql, return_response=True)
    repeated_entity_df = pd.DataFrame(repeated_entities)

    distinct_entities = repeated_entity_df['entity'].unique()
    for entity in distinct_entities:
        entitiesInfo[entity] = repeated_entity_df[repeated_entity_df['entity'] == entity].to_dict(orient='records')
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
    SELECT 
        a.author, 
        a.date, 
        a.title, 
        a.url, 
        string_agg(e.entity, ', ') as entities
    FROM public.article a 
    LEFT JOIN public.article_entities e on e.article_id = a.id 
    GROUP BY 1,2,3,4
    ORDER BY a.date DESC
    """
    all_articles = execute_sql(sql=sql, return_response=True)

    # if all_articles:
    #     for i, article in enumerate(all_articles):
    #         id = article[0]
    #         sql = """
    #         SELECT entity FROM public.v_articles_w_entities
    #         WHERE article_id = :id;
    #         """
    #         params = {'id': id}
    #         entities = execute_sql(sql=sql, params=params, return_response=True)
    #         entity_article = list(article)
    #         # stripping entities of () and converting to a single str
    #         if entities: entity_article.append(", ".join([entity[0] for entity in entities]))
    #         articles_w_entities.append(tuple(entity_article))

    return all_articles or []