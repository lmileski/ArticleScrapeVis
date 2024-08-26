import requests as r
import os
import local_config
dandelion_key = os.getenv('DANDELION_API_KEY', None)


def extract_entities(text: str) -> list:
    """
    returns a list of extracted entities for a given body of text.
    :param text: any body of text - in this case, a headline
    :returns list[str]
    """
    url = "https://api.dandelion.eu/datatxt/nex/v1"
    params = {
        'token': dandelion_key,
        'lang': 'en',
        'text': text,
        'min_confidence': 0.2,
    }
    response = r.get(
        url=url,
        params=params,
        verify=False
    )

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception(f"Unable to extract entities due to error: {response.text}")

    return [
        annotation['label']
        for annotation in response.json()['annotations']
    ]