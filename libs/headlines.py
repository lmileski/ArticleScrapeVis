import requests, os, sys
from datetime import datetime
sys.path.append('../ArticleScrapeVis')
import local_config

root = 'https://newsapi.org/v2'
api_key = os.getenv('NEWS_API_KEY')

def get_headlines() -> list[dict]:
    """
    Gets a list of US headlines from the API.
    Returns a list of dictionaries for each article, including:
        - author
        - title
        - date (as a datetime object)
        - URL
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

    return article_info