from pprint import pprint

import requests as req
import sys
address = " ".join(sys.argv[1:])


def quer(name, address=None):
    quer = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    params = {
        "apikey": api_key,
        "text": name,
        "lang": "en_US",
        'results': '1'
    }
    if address:
        params['ll'] = address
    return req.get(quer, params=params)


def find_apteka(name):
    response = quer(name)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['geometry']['coordinates']
    return coords


coords = find_apteka(address)
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": ", ".join(map(str, coords)),
    "format": "json",
    "kind": 'district',
    "results": '1'
}
response = req.get(geocoder_api_server, params=geocoder_params)

if not response:
    raise AttributeError(response.content)
res = response.json()
district = res["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']

print(f"{district} - район в котором находится '{address}'")
