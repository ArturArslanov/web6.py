import sys
from io import BytesIO
from pprint import pprint
import requests
from PIL import Image, ImageDraw, ImageFont
from funcs import find_apteka, find_spn, lonlat_distance

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    raise AttributeError(response.content)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = f"{find_spn(toponym_to_find)}"

apteka_coords, info = find_apteka(",".join([toponym_longitude, toponym_lattitude]))
distance = round(lonlat_distance(map(float, apteka_coords), (float(toponym_longitude), float(toponym_lattitude))))
info = f'{info}\ndistance - {distance} m'
print('\u2013')
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "l": "map",
    "pt": f'{",".join([toponym_longitude, toponym_lattitude])},pmdos1~{",".join(map(str, apteka_coords))},pmgns2',
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
im = Image.open(BytesIO(response.content))
draw_text = ImageDraw.Draw(im)
im.load()
draw_text.text((0, 100 - 60),
               info.split('\n')[0], fill=(100, 100, 100))
draw_text.text((0, 120 - 60),
               info.split('\n')[1], fill=(100, 100, 100))
draw_text.text((0, 140 - 60),
               info.split('\n')[2].replace('\u2013', '-'), fill=(100, 100, 100))
draw_text.text((0, 160 - 60),
               info.split('\n')[3], fill=(100, 100, 100))
im.show()
