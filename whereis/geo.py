from math import radians, cos, sin, asin, sqrt

from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

import requests


class LocationLookupError(Exception):
    """
    Raise where there is a problem looking up location data.
    """


def get_query_params(place_name, params=None):
    """
    Get a dictionary of API query parameters.
    """
    username = getattr(settings, "LOCATIONS_API_USERNAME", None)
    if not username:
        raise ImproperlyConfigured("The LOCATIONS_API_USERNAME setting is missing.")
    if params is None:
        params = {
            "username": "dimagi",
            "maxrows": 10,
            "type": "json",
            "lang": "en",
        }
    params["q"] = place_name
    return params


def query_api(name, url="http://api.geonames.org/search"):
    """
    Perform a query against the Geonames API.
    """
    params = get_query_params(name)
    response = requests.get(url, params=params)
    return response.json()


def find_location(email):
    """
    Attempt to return a full location record as a dictionary for a given email.
    Raises a ``LocationLookupError`` if anything goes wrong.
    """
    # FIXME: It may be desirable to refactor this into something less monlithic and more unit-testable.
    try:
        user = User.objects.get(email=email["address"])
    except User.DoesNotExist:
        raise LocationLookupError("Unknown user email: {}".format(email["address"]))
    result = query_api(email["subject"])
    if result["totalResultsCount"] == 0:
        raise LocationLookupError("Nothing matched the given location {}.".format(email["subject"]))
    # FIXME: Add the ability to choose different strategies for choosing a match.
    loc_data = result["geonames"][0]
    country = loc_data["countryName"]
    city = loc_data["name"] if loc_data["fclName"].startswith("city") else ""
    try:
        latitude = Decimal(loc_data["lat"])
        longitude = Decimal(loc_data["lng"])
    except InvalidOperation:
        raise LocationLookupError("The API returned an invalid lat/long position: {}, {}.".format(
            loc_data["lat"], loc_data["lng"]
        ))
    return {
        "user": user,
        "timestamp": email["date"],
        "raw_name": email["subject"],
        "country": country,
        "city": city,
        "latitude": latitude,
        "longitude": longitude,
    }


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).

    >>> #The distance between Jakarta and Richmond, VA is about 10,247 miles...
    >>> int(haversine(Decimal('106.84513'), Decimal('-6.21462'), Decimal('-77.46026'), Decimal('37.55376')))
    10247

    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # use haversine haversine formula to get the distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # 3956 miles is the great circle distance of earth
    return 3956 * c
