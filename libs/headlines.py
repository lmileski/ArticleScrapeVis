import requests, os
root = None
api_key = os.getenv('NEWS_API_KEY')


def get_headlines():
    """get a list of headlines from the API. US headlines only."""

