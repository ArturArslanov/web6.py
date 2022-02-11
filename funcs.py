from pprint import pprint
from math import radians, cos, sqrt

import requests as req


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = radians((a_lat + b_lat) / 2.)
    lat_lon_factor = cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = sqrt(dx * dx + dy * dy)
    return distance


def quer(name, address=None):
    quer = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    params = {
        "apikey": api_key,
        "text": name,
        "lang": "en_US",
        "type": "biz",
        'results': '1'
    }
    if address:
        params['ll'] = address
    return req.get(quer, params=params)


def find_apteka(address):
    response = quer('Аптека', address=address)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['geometry']['coordinates']
    # info = res['features'][0]['properties']['CompanyMetaData']
    # name = f"Pharmacy - {info['name']} \naddress: {info['address']}"
    # name = f"{name} \nwork time: {info['Hours']['text']}"
    return coords


def find_spn(toponym):
    response = quer(toponym)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['properties']['boundedBy']
    spn = max(abs(coords[1][0] - coords[0][0]), abs(coords[1][1] - coords[0][1]))
    return spn
