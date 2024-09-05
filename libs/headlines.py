import requests, os
import pandas as pd
from datetime import datetime

root = 'https://newsapi.org/v2'
api_key = os.getenv('NEWS_API_KEY')
verify_requests = int(os.getenv('VERIFY_REQUESTS'))


def get_headlines() -> list:
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
    response = requests.get(url, params=params, verify=verify_requests).json()

    # parsing response - collecting only author/title/date/URL
    article_info: list[dict] = []
    for article in response['articles']:
        date_str = article['publishedAt']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

        required_article_info = {
            'author': article['author'] if article['author'] else 'Unknown',
            'title': article['title'],
            'date': date_obj,
            'url': article['url']
        }

        article_info.append(required_article_info)

    return article_info