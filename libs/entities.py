"""
Gets a collection of headlines and generates extracted entities for each of them,
then puts inserts all entities into entity table in postgres database
"""

from libs.dandelion import extract_entities
from libs.db import execute_sql

def add_entities(headline_titles: list[str]) -> None:

    entities_insertion = ""
    insertion_params = {}
    insertion_key = 1

    # adding entities to dbo.article_entities table
    for headline_text in headline_titles:
        entities: list[str] = extract_entities(headline_text)
        # finding matching article id - foreign key
        id_key = execute_sql(
            sql = f"SELECT id FROM article WHERE title = :headline",
            params = {'headline': headline_text},
            table_name = 'article_entities',
            return_response = True
            )
        # adding to sql insertion for each entity
        for entity in entities:
            entities_insertion += f"""
            INSERT INTO article_entities (article_id, entity)
            VALUES (:key{insertion_key}, :entity{insertion_key});
            """
            insertion_params[f'key{insertion_key}'] = id_key[0][0] # type: ignore
            insertion_params[f'entity{insertion_key}'] = entity

            insertion_key += 1
        
    execute_sql(sql=entities_insertion, params=insertion_params, commit=True)