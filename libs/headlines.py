import requests, os
import pandas as pd
from datetime import datetime
import local_config
from libs.db import execute_sql

root = 'https://newsapi.org/v2'
api_key = os.getenv('NEWS_API_KEY')

def add_headlines() -> pd.DataFrame:
    """
    Gets a list of US headlines from the API, including
    a list of dictionaries for each article:
        - author
        - title
        - date (as a datetime object)
        - URL
    Adds all this info to the postgres db
    Return the pandas df from the list of dictionaries
    """
    # collecting data w/ API
    url = f'{root}/top-headlines'
    params = {'country': 'us', 'apiKey': api_key}
    response = requests.get(url, params=params).json()

    # parsing response - collecting only author/title/date/URL
    article_info: list[dict] = []
    for article in response['articles']:
        date_str = article['publishedAt']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

        required_article_info = {
            'author': article['author'],
            'title': article['title'],
            'date': date_obj,
            'url': article['url']
        }

        article_info.append(required_article_info)

    df = pd.DataFrame(article_info)

    # executing headline info to db
    execute_sql(df=df, table_name='article', commit=True)

    return df