import requests
from time import time, sleep
import json
import random
import requests
import shutil

ip_address = '109.248.175.95'

exhibit_parsed = False

while True:
    images = 100
    i=0
    while i<images:
        while exhibit_parsed == False:
            random_exhibit = random.randint(0,4500000)
            exh = requests.get(f'https://goskatalog.ru/muzfo-rest/rest/exhibits/{random_exhibit}')
            exh = json.loads(exh.content)
            if 'name' in exh:
                exh_images = exh['images']
                im_link = None
                if len(exh_images)>0:
                    exh_image_id = exh_images[0]['id']
                    im_link = 'https://goskatalog.ru/muzfo-imaginator/rest/images/original/'+str(exh_image_id)
                    exhibit_parsed = True

        im_response = requests.get(im_link, stream=True)
        with open('test_img.png', 'wb') as out_file:
            shutil.copyfileobj(im_response.raw, out_file)
        del im_response

        exhibit_data = {
            'exh_id':random_exhibit,
            'name':exh['name'],
            'description':'' if exh['description'] is None else exh['description'] ,
        }

        multiple_files = [('files', ('test_img.png', open('./test_img.png', 'rb')))]


        exhibit = requests.post(f'http://{ip_address}:8000/api/exhibits/add', params=exhibit_data, files=multiple_files)
        i+=1
        exhibit_parsed = False
        print(i)