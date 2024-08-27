from setup.tables import create_tables
from libs.headlines import add_headlines
from libs.entities import add_entities
from libs.join_tables import create_joint_table

"""
- update_db() creates all tables if they aren't already made
- insert_data() adds all article headline and entity info into the database

Also used as script for frequent db updates through Heroku
"""

def update_db(reset=False):
    """
    Creates needed db tables if they don't already exist
    When reset=True, all table data is erased
    """
    sql = ""

    if reset:
        sql += """
        TRUNCATE TABLE IF EXISTS public.article CASCADE;
        TRUNCATE TABLE IF EXISTS public.article_entities CASCADE;
        TRUNCATE TABLE IF EXISTS public.entities_to_articles;
        """
    
    create_tables(sql=sql)

def insert_data():
    """
    Inserts all the most recent API scraped article and
    headline info to the database
    """
    # clearing old table info if existent
    update_db(reset=True)
    # inserts headline data and returns the used df
    top_headlines = add_headlines()
    # adding entity data based off titles of headlines in the df
    add_entities(list(top_headlines['title']))
    # creating the joint table with newest info
    create_joint_table()

if __name__ == '__main__':
    update_db()