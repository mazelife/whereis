import requests


def get_query_params(place_name, params=None):
    if params is None:
        params = {
            "username": "dimagi",
            "maxrows": 10,
            "type": "json",
            "lang": "en",
        }
    params["q"] = place_name
    return params


def lookup_name(name, url="http://api.geonames.org/search"):
     params=get_query_params(name)
     response = requests.get(url, params=params)
     return response.json()
