import requests as req


def find_spn(toponym):
    quer = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    params = {
        "apikey": api_key,
        "text": toponym,
        "lang": "ru_RU",
        "type": "biz",
        'results': '1'
    }
    response = req.get(quer, params=params)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['properties']['boundedBy']
    spn = max(abs(coords[1][0] - coords[0][0]), abs(coords[1][1] - coords[0][1]))
    return spn
