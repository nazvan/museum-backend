import requests
from time import time, sleep
import json
import random
import requests

ip_address = '109.248.175.95'

exhibit_parsed = False

while not exhibit_parsed:
    random_exhibit = random.randint(0,4500000)
    # random_exhibit = 50540160 # Статуэтка "любопытство" с описанием

    exh = requests.get(f'https://goskatalog.ru/muzfo-rest/rest/exhibits/{random_exhibit}')
    exh = json.loads(exh.content)
    if 'name' in exh:
        exhibit_parsed = True

    print(exh)

print(random_exhibit)

exh_images = exh['images']
im_link = None
if len(exh_images)>0:
    exh_image_id = exh_images[0]['id']
    im_link = 'https://goskatalog.ru/muzfo-imaginator/rest/images/original/'+str(exh_image_id)

exhibit_data = {
    'exh_id':random_exhibit,
    'name':exh['name'],
    'type_id':0,
    'desc':exh['description'],
    'url':im_link,
    'timestamp':int(time()),
    'image_path':'backend image path'
}
print(exhibit_data)

exhibit = requests.post(f'http://{ip_address}:8000/api/exhibits/add', json=exhibit_data)
print(exhibit.content)