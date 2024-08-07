import requests, os
root = 'https://api.currentsapi.services/v1'
api_key = os.getenv('CURRENTS_API_KEY')


def get_headlines():
    """get a list of headlines from the API. US headlines only."""
    url = f'{root}/latest-news'
    params = {
        'language': 'us',
        'apiKey': api_key
    }

    # 200 -> ok
    # 400 -> malformed request
    # 500 -> ???
    response = requests.get(url, params=params, verify=False).json()
    return response





